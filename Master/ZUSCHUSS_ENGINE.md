=LET(
  config_lk; IFERROR(VLOOKUP(target_lk; CONFIG!A:B; 2; 0); target_lk);
  setup_event_typ; TRIM(setup_key);
  rule_key; config_lk & "_" & SUBSTITUTE(setup_event_typ; " "; "_");
  
  get_rule; LAMBDA(idx; IFERROR(VLOOKUP(rule_key; CACHE_RULES!A:X; idx; 0); ""));
  
  kuerzel; get_rule(4);
  
  min_tn; LET(v; get_rule(5); IF(v=""; 0; VALUE(v)));
  min_alter_tn; LET(v; get_rule(6); IF(v=""; 0; VALUE(v)));
  max_alter_tn; LET(v; get_rule(7); IF(v=""; 999; VALUE(v)));
  min_alter_soft; LET(v; get_rule(8); IF(v=""; min_alter_tn; VALUE(v)));
  min_tage; LET(v; get_rule(9); IF(v=""; 0; VALUE(v)));
  
  min_quote; LET(v; get_rule(10); IF(v=""; 0; VALUE(v)));
  quote_modus; LET(v; get_rule(11); IF(v=""; "MEHRHEIT"; TRIM(v)));
  quote_aktion; LET(v; get_rule(12); IF(v=""; "NUR_LOKALE"; TRIM(v)));
  
  target_groups; LET(v; get_rule(13); IF(v=""; "TN;MA;LEITUNG;REF"; TRIM(v)));
  tg_local_only; LET(v; get_rule(14); IF(v=""; "TN"; TRIM(v)));
  quote_bezug; LET(v; get_rule(15); IF(v=""; "TN"; TRIM(v)));
  
  alter_config; get_rule(16);
  label_map; get_rule(17);
  
  output_cols_def; get_rule(18);
  sort_order; LET(v; get_rule(19); IF(v=""; "LOKAL_FIRST;ALPHA"; TRIM(v)));
  filter_function; LET(v; get_rule(20); IF(v=""; "ALL"; TRIM(v)));
  
  property_map; get_rule(21);
  status_filter; LET(v; get_rule(22); IF(v=""; "Angemeldet"; TRIM(v)));
  min_anwesenheit; LET(v; get_rule(23); IF(v=""; 0; VALUE(v)));
  zonen_config; LET(z; get_rule(24); IF(z=""; "3-749;754-1454;1459-1710"; z));
  
  event_dauer; IFERROR(DATEDIF(event_start; event_end; "D") + 1; 0);
  tage_check_ok; OR(min_tage = 0; event_dauer >= min_tage);
  
  headers; TN_LISTE!2:2; 
  active_zone; IF(ISOMITTED(zone); 1; zone);
  
  zone_parts; SPLIT(zonen_config; ";");
  current_zone; INDEX(zone_parts; 1; active_zone);
  range_limits; SPLIT(current_zone; "-");
  row_start; INDEX(range_limits; 1; 1);
  row_end; INDEX(range_limits; 1; 2);
  
  full_data; tn_range;
  rows_total; ROWS(full_data);
  rows_seq; SEQUENCE(rows_total); 
  data_zone; FILTER(full_data; (rows_seq >= (row_start-2)) * (rows_seq <= (row_end-2)));

  find_col_idx; LAMBDA(name; 
    LET(
      exact; MATCH(name; headers; 0);
      wild; MATCH("*" & name & "*"; headers; 0);
      clean; MATCH(SUBSTITUTE(name; "-"; "*"); headers; 0);
      clean2; MATCH(SUBSTITUTE(name; "_"; " "); headers; 0);
      raw_idx; IF(ISNUMBER(exact); exact; IF(ISNUMBER(wild); wild; IF(ISNUMBER(clean); clean; IF(ISNUMBER(clean2); clean2; 0))));
      IF(raw_idx > 0; raw_idx - 1; 0)
    )
  );
  
  idx_status; find_col_idx("Status");
  idx_fn; find_col_idx("Funktion");
  idx_lk; find_col_idx("Landkreis");
  idx_alter; find_col_idx("Alter");
  idx_anwesenheit; find_col_idx("Anwesenheit");
  idx_sort; find_col_idx("Nachname");
  
  critical_missing; OR(idx_status=0; idx_fn=0; idx_lk=0);
  
  base_mask; MAP(INDEX(data_zone;;idx_status); INDEX(data_zone;;idx_fn); LAMBDA(s; f;
     AND(
       s = status_filter;
       ISNUMBER(SEARCH(f; target_groups))
     )
  ));
  base_filtered; FILTER(data_zone; base_mask);
  
  filter_fn_mask; IF(filter_function = "ALL";
    SEQUENCE(ROWS(base_filtered); 1; 1; 0);
    MAP(INDEX(base_filtered;;idx_fn); LAMBDA(fn;
      IF(filter_function = "TN_ONLY"; fn = "TN";
        IF(filter_function = "STAFF_ONLY"; OR(fn = "MA"; fn = "LEITUNG");
          IF(filter_function = "REF_ONLY"; fn = "REF";
            IF(filter_function = "TN_MA"; OR(fn = "TN"; fn = "MA");
              TRUE
            )
          )
        )
      )
    ))
  );
  fn_filtered; FILTER(base_filtered; filter_fn_mask);
  
  alter_mask; IF(idx_alter = 0; 
    SEQUENCE(ROWS(fn_filtered); 1; 1; 0);
    MAP(INDEX(fn_filtered;;idx_fn); INDEX(fn_filtered;;idx_alter); LAMBDA(fn; alter_val;
      LET(
        alter; IFERROR(VALUE(alter_val); 0);
        IF(fn = "TN";
          AND(alter >= min_alter_soft; alter <= max_alter_tn);
          IF(alter_config = ""; TRUE;
            LET(
              pattern; fn & ":([0-9]+)-([0-9]+)";
              has_config; REGEXMATCH(alter_config; pattern);
              IF(NOT(has_config); TRUE;
                LET(
                  extracted; REGEXEXTRACT(alter_config; pattern);
                  min_a; VALUE(INDEX(extracted; 1; 1));
                  max_a; VALUE(INDEX(extracted; 1; 2));
                  AND(alter >= min_a; alter <= max_a)
                )
              )
            )
          )
        )
      )
    ))
  );
  alter_filtered; FILTER(fn_filtered; alter_mask);
  
  anwesenheit_mask; IF(OR(idx_anwesenheit = 0; min_anwesenheit = 0);
    SEQUENCE(ROWS(alter_filtered); 1; 1; 0);
    MAP(INDEX(alter_filtered;;idx_anwesenheit); LAMBDA(aw;
      IFERROR(VALUE(aw); 0) >= min_anwesenheit
    ))
  );
  anwesenheit_filtered; FILTER(alter_filtered; anwesenheit_mask);

  quote_relevant_mask; MAP(INDEX(anwesenheit_filtered;;idx_fn); LAMBDA(fn;
    ISNUMBER(SEARCH(fn; quote_bezug))
  ));
  quote_relevant_data; IFERROR(FILTER(anwesenheit_filtered; quote_relevant_mask); "");
  
  total_for_quote; IF(quote_relevant_data = ""; 0; ROWS(quote_relevant_data));
  
  lokale_for_quote; IF(total_for_quote = 0; 0;
    SUMPRODUCT(MAP(INDEX(quote_relevant_data;;idx_lk); LAMBDA(lk; IF(lk = config_lk; 1; 0))))
  );
  
  quote_pct; IF(total_for_quote = 0; 0; lokale_for_quote / total_for_quote * 100);
  
  quote_erfuellt; IF(quote_modus = "MEHRHEIT";
    lokale_for_quote > total_for_quote - lokale_for_quote;
    quote_pct >= min_quote
  );
  
  use_all; OR(
    quote_aktion = "ALLE_IMMER";
    AND(quote_aktion = "ALLE_WENN_ERFUELLT"; quote_erfuellt)
  );

  wohnort_mask; MAP(INDEX(anwesenheit_filtered;;idx_fn); INDEX(anwesenheit_filtered;;idx_lk); LAMBDA(fn; lk;
    OR(
      use_all;
      NOT(ISNUMBER(SEARCH(fn; tg_local_only)));
      lk = config_lk
    )
  ));
  wohnort_filtered; FILTER(anwesenheit_filtered; wohnort_mask);

  has_lokal_first; ISNUMBER(SEARCH("LOKAL_FIRST"; sort_order));
  has_fn_sort; ISNUMBER(SEARCH("FUNKTION"; sort_order));
  
  is_local_col; MAP(INDEX(wohnort_filtered;;idx_lk); LAMBDA(lk; IF(lk = config_lk; 0; 1)));
  
  sorted_data; IF(AND(has_fn_sort; has_lokal_first);
    LET(
      with_sort; HSTACK(INDEX(wohnort_filtered;;idx_fn); is_local_col; wohnort_filtered);
      sorted; SORT(with_sort; 1; 1; 2; 1; 3+idx_sort; 1);
      CHOOSECOLS(sorted; SEQUENCE(1; COLUMNS(wohnort_filtered); 3))
    );
    IF(has_lokal_first;
      LET(
        with_sort; HSTACK(is_local_col; wohnort_filtered);
        sorted; SORT(with_sort; 1; 1; 1+idx_sort; 1);
        CHOOSECOLS(sorted; SEQUENCE(1; COLUMNS(wohnort_filtered); 2))
      );
      IF(has_fn_sort;
        SORT(wohnort_filtered; idx_fn; 1; idx_sort; 1);
        IF(sort_order = "KEINE"; 
          wohnort_filtered;
          SORT(wohnort_filtered; idx_sort; 1)
        )
      )
    )
  );

  final_tn_count; ROWS(sorted_data);
  min_tn_ok; OR(min_tn = 0; final_tn_count >= min_tn);

  out_cols_list; SPLIT(output_cols_def; ";");
  num_out_cols; COLUMNS(out_cols_list);
  cnt_rows; ROWS(sorted_data);
  
  get_val_by_header; LAMBDA(row_data; h_name;
    LET(
      idx; find_col_idx(h_name);
      idx_alt; IF(idx > 0; idx;
        IF(h_name = "Geburtsdatum"; find_col_idx("Geburtstag");
          IF(h_name = "Geburtstag"; find_col_idx("Geburtsdatum");
            IF(h_name = "Ort"; find_col_idx("Wohnort");
              IF(h_name = "Wohnort"; find_col_idx("Ort"); 0)
            )
          )
        )
      );
      final_idx; IF(idx > 0; idx; idx_alt);
      IF(final_idx > 0; INDEX(row_data; 1; final_idx); "")
    )
  );

  apply_label_map; LAMBDA(original; map_str;
    IF(map_str = ""; original;
      LET(
        parts; SPLIT(map_str; ";");
        num_parts; COLUMNS(parts);
        result; REDUCE(original; SEQUENCE(1; num_parts); LAMBDA(acc; i;
          LET(
            part; TRIM(INDEX(parts; 1; i));
            kv; IFERROR(SPLIT(part; "="); "");
            key; IF(kv = ""; ""; TRIM(INDEX(kv; 1; 1)));
            val; IF(kv = ""; ""; IFERROR(TRIM(INDEX(kv; 1; 2)); key));
            IF(acc = key; val; acc)
          )
        ));
        result
      )
    )
  );

  apply_property_map; LAMBDA(original; map_str;
    IF(OR(map_str = ""; original = ""; original = "--"); "";
      LET(
        parts; SPLIT(map_str; ";");
        num_parts; COLUMNS(parts);
        result; REDUCE(original; SEQUENCE(1; num_parts); LAMBDA(acc; i;
          LET(
            part; TRIM(INDEX(parts; 1; i));
            kv; IFERROR(SPLIT(part; "="); "");
            key; IF(kv = ""; ""; TRIM(INDEX(kv; 1; 1)));
            val; IF(kv = ""; ""; IFERROR(TRIM(INDEX(kv; 1; 2)); key));
            IF(acc = key; val; acc)
          )
        ));
        result
      )
    )
  );

  simple_eval; LAMBDA(row_data; tmpl;
    LET(
      t_trim; TRIM(tmpl);
      is_year; ISNUMBER(SEARCH("YEAR("; t_trim));
      is_text; ISNUMBER(SEARCH("TEXT("; t_trim));
      
      text_fmt; IF(is_text; 
        IFERROR(REGEXEXTRACT(t_trim; ",\s*""(.*)""\)$"); "DD.MM.YYYY"); 
        ""
      );
      
      base_tmpl; IF(is_year; 
        MID(t_trim; 6; LEN(t_trim)-6); 
        IF(is_text;
           IFERROR(REGEXEXTRACT(t_trim; "TEXT\((.*?),"); t_trim);
           t_trim
        )
      );
      
      val_vn; get_val_by_header(row_data; "Vorname");
      val_nn; get_val_by_header(row_data; "Nachname");
      val_wo; get_val_by_header(row_data; "Wohnort");
      val_lk; get_val_by_header(row_data; "Landkreis");
      val_gd; get_val_by_header(row_data; "Geburtsdatum");
      val_an; get_val_by_header(row_data; "Anwesenheit");
      val_plz; get_val_by_header(row_data; "PLZ");
      val_ort; get_val_by_header(row_data; "Ort");
      val_str; get_val_by_header(row_data; "Straße");
      val_fn_raw; get_val_by_header(row_data; "Funktion");
      val_fn; apply_label_map(val_fn_raw; label_map);
      val_alter; get_val_by_header(row_data; "Alter");
      val_geschlecht; get_val_by_header(row_data; "Geschlecht");
      val_bundesland; get_val_by_header(row_data; "Bundesland");
      val_juleica_raw; get_val_by_header(row_data; "Juleica");
      val_juleica; apply_label_map(val_juleica_raw; label_map);
      val_behinderung_raw; get_val_by_header(row_data; "Behinderung");
      val_behinderung; apply_property_map(val_behinderung_raw; property_map);

      repl_1; SUBSTITUTE(base_tmpl; "{Vorname}"; val_vn);
      repl_2; SUBSTITUTE(repl_1; "{Nachname}"; val_nn);
      repl_3; SUBSTITUTE(repl_2; "{Wohnort}"; val_wo);
      repl_4; SUBSTITUTE(repl_3; "{Landkreis}"; val_lk);
      repl_5; SUBSTITUTE(repl_4; "{Geburtsdatum}"; val_gd);
      repl_6; SUBSTITUTE(repl_5; "{Anwesenheit}"; val_an);
      repl_7; SUBSTITUTE(repl_6; "{PLZ}"; val_plz);
      repl_8; SUBSTITUTE(repl_7; "{Ort}"; val_ort);
      repl_9; SUBSTITUTE(repl_8; "{Straße}"; val_str);
      repl_10; SUBSTITUTE(repl_9; "{Funktion}"; val_fn);
      repl_11; SUBSTITUTE(repl_10; "{Alter}"; val_alter);
      repl_12; SUBSTITUTE(repl_11; "{Geschlecht}"; val_geschlecht);
      repl_13; SUBSTITUTE(repl_12; "{Bundesland}"; val_bundesland);
      repl_14; SUBSTITUTE(repl_13; "{Juleica}"; val_juleica);
      repl_15; SUBSTITUTE(repl_14; "{Behinderung}"; val_behinderung);
      
      final_res; IF(is_year;
         LET(
           raw; repl_15; 
           v_num; IFERROR(VALUE(raw); 0);
           y_from_serial; IF(v_num > 10000; YEAR(v_num); 0);
           y_from_date; IFERROR(YEAR(DATEVALUE(raw)); 0);
           y_final; IF(y_from_serial > 0; y_from_serial; y_from_date);
           IF(y_final < 1920; ""; "" & y_final)
         );
         IF(is_text;
           LET(
             raw; repl_15;
             v_num; IFERROR(VALUE(raw); 0);
             d_val; IF(v_num > 10000; v_num; IFERROR(DATEVALUE(raw); 0));
             IF(d_val > 0; TEXT(d_val; text_fmt); raw)
           );
           repl_15
         )
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
  
  debug_output; VSTACK(
    HSTACK("Rule Key:"; rule_key);
    HSTACK("Kuerzel:"; kuerzel);
    HSTACK("Quote:"; ROUND(quote_pct; 1) & "% (" & lokale_for_quote & "/" & total_for_quote & ")");
    HSTACK("Quote erfüllt:"; IF(quote_erfuellt; "JA"; "NEIN"));
    HSTACK("Use All:"; IF(use_all; "JA"; "NEIN"));
    HSTACK("Finale TN:"; final_tn_count)
  );

  error_msg; IF(NOT(tage_check_ok); 
    "FEHLER: Event-Dauer (" & event_dauer & " Tage) < MIN_TAGE (" & min_tage & ")";
    IF(NOT(min_tn_ok);
      "HINWEIS: Nur " & final_tn_count & " TN (MIN_TN=" & min_tn & " nicht erreicht)";
      ""
    )
  );

  IF(critical_missing; 
    "FEHLER: ZUSCHUSS_ENGINE Init fehlgeschlagen (Spalten fehlen)"; 
    IF(debug; 
      debug_output;
      IF(error_msg <> ""; error_msg;
        IF(cnt_rows=0; "Keine Daten nach Filter"; result)
      )
    )
  )
)
