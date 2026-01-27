=LET(
  /* 1. PARAMETER MAPPING (Named Function Inputs) */
  /* tn_range, setup_key, target_lk, event_start, debug */
  
  /* CONFIG LOAD */
  config_lk; IFERROR(VLOOKUP(target_lk; CONFIG!A:B; 2; 0); "CONFIG_ERROR");
  setup_event_typ; TRIM(setup_key);
  rule_key; config_lk & "_" & SUBSTITUTE(setup_event_typ; " "; "_");
  
  /* RULES LOAD */
  get_rule; LAMBDA(idx; IFERROR(VLOOKUP(rule_key; CACHE_RULES!A:X; idx; 0); ""));
  
  /* Rules Definitions */
  target_groups; LET(v; get_rule(13); IF(OR(v=""; v="--"; v="NOT_FOUND"); "TN;MA;LEITUNG;REF"; TRIM(v)));
  status_filter; LET(s; get_rule(22); IF(s=""; "Angemeldet"; TRIM(s)));
  zonen_config; LET(z; get_rule(24); IF(z=""; "3-749;754-1454;1459-1710"; z));
  output_cols_def; get_rule(18); /* Das ist der Direct Data Definition String */
  
  /* DATA SETUP */
  /* Wir nehmen an, tn_range ist B3:AQxxx => Header sind in Zeile 2 */
  /* V7 Standard: TN_LISTE!2:2 ist IMMER Header */
  headers; TN_LISTE!2:2; 
  
  /* ZONEN LOGIK */
  /* zone parameter nutzen, default 1 */
  active_zone; IF(ISOMITTED(zone); 1; zone);
  
  zone_parts; SPLIT(zonen_config; ";");
  current_zone; INDEX(zone_parts; 1; active_zone);
  range_limits; SPLIT(current_zone; "-");
  row_start; INDEX(range_limits; 1; 1);
  row_end; INDEX(range_limits; 1; 2);
  
  /* FILTER RANGE */
  /* tn_range sollte die komplette Tabelle sein */
  full_data; tn_range;
  rows_total; ROWS(full_data);
  rows_seq; SEQUENCE(rows_total); 
  
  /* Achtung: Row Indizes in Config sind absolut (z.B. 3-749). */
  /* Wenn tn_range bei 3 beginnt, ist Index 1 = Zeile 3. */
  /* Mapping: Index = Zeile - 2. */
  data_zone; FILTER(full_data; (rows_seq >= (row_start-2)) * (rows_seq <= (row_end-2)));

  /* HELPER */
  find_col_idx; LAMBDA(name; 
    LET(
      exact; MATCH(name; headers; 0);
      wild; MATCH("*" & name & "*"; headers; 0);
      clean; MATCH(SUBSTITUTE(name; "-"; "*"); headers; 0);
      clean2; MATCH(SUBSTITUTE(name; "_"; " "); headers; 0);
      /* Offset -1 weil Range bei B beginnt, Header aber bei A? Check TN_LISTE Struktur. */
      /* TN_LISTE B:AQ. MATCH auf 2:2. */
      /* Wenn Header bei B2 anfängt, ist MATCH("Status", 2:2) z.B. 2. */
      /* INDEX(tn_range, ..., 1) greift auf B zu (Spalte 1 des Ranges). */
      /* Also Korrekturfaktor: MATCH - 1 (wenn A Spalte 1 ist) */
      raw_idx; IF(ISNUMBER(exact); exact; IF(ISNUMBER(wild); wild; IF(ISNUMBER(clean); clean; IF(ISNUMBER(clean2); clean2; 0))));
      IF(raw_idx > 0; raw_idx - 1; 0)
    )
  );
  
  idx_status; find_col_idx("Status");
  idx_fn; find_col_idx("Funktion");
  idx_lk; find_col_idx("Landkreis");
  
  critical_missing; OR(idx_status=0; idx_fn=0; idx_lk=0);
  
  /* FILTER CORE */
  filter_mask; MAP(INDEX(data_zone;;idx_status); INDEX(data_zone;;idx_fn); INDEX(data_zone;;idx_lk); LAMBDA(s; f; l;
     AND(
       s = status_filter;
       ISNUMBER(SEARCH(f; target_groups));
       l = config_lk
     )
  ));
  
  filtered_data; FILTER(data_zone; filter_mask);
  
  idx_sort; find_col_idx("Nachname");
  sorted_data; IF(idx_sort>0; SORT(filtered_data; idx_sort; TRUE); filtered_data);

  /* OUTPUT GENERATION */
  out_cols_list; SPLIT(output_cols_def; ";");
  num_out_cols; COLUMNS(out_cols_list);
  cnt_rows; ROWS(sorted_data);
  
  get_val_by_header; LAMBDA(row_data; h_name;
    LET(idx; find_col_idx(h_name); IF(idx>0; INDEX(row_data; 1; idx); ""))
  );

  simple_eval; LAMBDA(row_data; tmpl;
    LET(
      t_trim; TRIM(tmpl);
      is_year; ISNUMBER(SEARCH("YEAR("; t_trim));
      base_tmpl; IF(is_year; REGEXEXTRACT(t_trim; "YEAR\((.*)\)"); t_trim);
      
      val_vn; get_val_by_header(row_data; "Vorname");
      val_nn; get_val_by_header(row_data; "Nachname");
      val_wo; get_val_by_header(row_data; "Wohnort");
      val_lk; get_val_by_header(row_data; "Landkreis");
      val_gd; get_val_by_header(row_data; "Geburtsdatum");
      val_an; get_val_by_header(row_data; "Anwesenheit");
      val_plz; get_val_by_header(row_data; "PLZ");
      val_ort; get_val_by_header(row_data; "Ort");
      val_str; get_val_by_header(row_data; "Straße");

      repl_1; SUBSTITUTE(base_tmpl; "{Vorname}"; val_vn);
      repl_2; SUBSTITUTE(repl_1; "{Nachname}"; val_nn);
      repl_3; SUBSTITUTE(repl_2; "{Wohnort}"; val_wo);
      repl_4; SUBSTITUTE(repl_3; "{Landkreis}"; val_lk);
      repl_5; SUBSTITUTE(repl_4; "{Geburtsdatum}"; val_gd);
      repl_6; SUBSTITUTE(repl_5; "{Anwesenheit}"; val_an);
      repl_7; SUBSTITUTE(repl_6; "{PLZ}"; val_plz);
      repl_8; SUBSTITUTE(repl_7; "{Ort}"; val_ort);
      repl_9; SUBSTITUTE(repl_8; "{Straße}"; val_str);
      
      final_res; IF(is_year;
         LET(
           raw; repl_9; 
           v_num; IFERROR(VALUE(raw); 0);
           y_from_serial; IF(v_num > 10000; YEAR(v_num); 0);
           y_from_date; IFERROR(YEAR(DATEVALUE(raw)); 0);
           y_final; IF(y_from_serial > 0; y_from_serial; y_from_date);
           IF(y_final < 1920; ""; "" & y_final)
         );
         repl_9
      );
      final_res
    )
  );

  result; MAKEARRAY(cnt_rows; num_out_cols; LAMBDA(r; c;
    LET(
      tmpl_str; INDEX(out_cols_list; 1; c);
      row_d; INDEX(sorted_data; r);
      simple_eval(row_d; tmpl_str)
    )
  ));
  
  IF(critical_missing; "FEHLER: ZUSCHUSS_ENGINE Init fehlgeschlagen (Spalten fehlen)"; IF(cnt_rows=0; "Keine Daten"; result))
)
