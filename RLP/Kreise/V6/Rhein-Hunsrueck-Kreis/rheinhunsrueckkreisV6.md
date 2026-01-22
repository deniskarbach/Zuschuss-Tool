# Formel für Rhein-Hunsrück-Kreis V6

**Status:** ✅ v6 – Fragmentiertes Layout (TN1, TN2, MA, REF)  
**Kürzel:** SIM

## Layout-Übersicht

Das Layout ist in 4 Bereiche unterteilt. Jeder Bereich benötigt eine **eigene Formel**.

| Bereich | Zelle | Inhalt | Zeilen | Kapazität | Logik |
|---|---|---|---|---|---|
| **TN 1** | **B4** | Teilnehmer 1-22 | 4-25 | 22 | `type="TN"`, `offset=0` |
| **TN 2** | **B28** | Teilnehmer 23-32 | 28-37 | 10 | `type="TN"`, `offset=22` |
| **MA** | **B40** | Betreuer 1-6 | 40-45 | 6 | `type="MA"`, `offset=0` |
| **REF** | **B49** | Referenten 1-2 | 49-50 | 2 | `type="REF"`, `offset=0` |

---

## Output-Spalten (TN & MA)

| Spalte | Feld | Quelle |
|--------|------|--------|
| A | Lfd. Nr | *separat* |
| B | Vor- und Zuname | Index 13 + 12 |
| C | PLZ Wohnort | Index 16 + 17 (Format: "PLZ Ort") |
| D | Geburtsdatum | Index 14 (dd.MM.yyyy) |
| E | Veranst.- tage | Index 6 |
| F | Übernachtungen | Index 6 - 1 |
| G | Unterschrift | leer |

## Output-Spalten (REF)

| Spalte | Feld | Quelle |
|--------|------|--------|
| B | Vor- und Zuname | Index 13 + 12 |
| C | PLZ Wohnort | Index 16 + 17 |
| D | Mind. 2 Std | leer |
| E | Mind. 4 Std | leer |
| F | Thema | leer |

---

## CACHE_RULES Keys

| Key | Event-Typ |
|-----|-----------|
| `Landkreis Rhein-Hunsrück-Kreis_Soziale_Bildung` | Soziale_Bildung |
| `Landkreis Rhein-Hunsrück-Kreis_Schulung_Ehrenamtlicher_Mitarbeitenden` | Schulung |
| `Landkreis Rhein-Hunsrück-Kreis_Politische_Jugendbildung` | Politische_Jugendbildung |

---

## Teil 1 – TN Liste (Zelle B4)

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  target_type; "TN";
  page_size; 22;
  start_offset; 0;
  
  start_idx; start_offset + 1;
  end_idx; start_offset + page_size;
  
  ziel_landkreis; "Landkreis Rhein-Hunsrück-Kreis";
  event_typ_raw; SETUP!B18;
  event_start; SETUP!B23;
  event_ende; SETUP!H23;
  cache_rules; CACHE_RULES!A:Z;
  clean_landkreis; TRIM(CLEAN(ziel_landkreis));
  clean_event; SUBSTITUTE(TRIM(CLEAN(event_typ_raw)); " "; "_");
  rule_key; clean_landkreis & "_" & clean_event;
  
  event_tage; LET(
    start_num; IF(ISNUMBER(event_start); event_start; IFERROR(DATEVALUE(event_start); 0));
    ende_num; IF(ISNUMBER(event_ende); event_ende; IFERROR(DATEVALUE(event_ende); 0));
    IF(AND(start_num > 0; ende_num > 0); ende_num - start_num + 1; 0)
  );
  
  raw_z1; TN_LISTE!B3:AC749;
  raw_z2; TN_LISTE!B754:AC1454;
  raw_z3; TN_LISTE!B1459:AC1710;
  
  status_z1; TN_LISTE!B3:B749;
  status_z2; TN_LISTE!B754:B1454;
  status_z3; TN_LISTE!B1459:B1710;
  
  lk_z1; TN_LISTE!AB3:AB749;
  lk_z2; TN_LISTE!AB754:AB1454;
  lk_z3; TN_LISTE!AB1459:AB1710;
  
  get_rule; LAMBDA(col; IFERROR(VLOOKUP(rule_key; cache_rules; col; 0); "NOT_FOUND"));
  rule_check; get_rule(1);
  
  foerder_umfang; LET(v; get_rule(5); IF(OR(v=""; v="--"; v="NOT_FOUND"); "TN_K"; TRIM(v)));
  min_tn; LET(v; get_rule(6); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_alter; LET(v; get_rule(7); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  max_alter; LET(v; get_rule(8); IF(OR(v=""; v="--"; v="NOT_FOUND"); 999; VALUE(v)));
  min_alter_soft; LET(v; get_rule(9); IF(OR(v=""; v="--"; v="NOT_FOUND"); min_alter; VALUE(v)));
  min_tage; LET(v; get_rule(10); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote_raw; LET(v; get_rule(11); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote; IF(min_quote_raw > 1; min_quote_raw / 100; min_quote_raw);
  quote_modus; LET(v; get_rule(12); IF(OR(v=""; v="--"; v="NOT_FOUND"); "MEHRHEIT"; UPPER(TRIM(v))));
  logik_modus; LET(v; get_rule(13); IF(OR(v=""; v="--"; v="NOT_FOUND"); "Standard"; TRIM(v)));
  
  tn_kreis; OR(foerder_umfang="TN_K"; foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF");
  tn_pauschal; OR(foerder_umfang="TN_P"; foerder_umfang="TN_P_MA_K"; foerder_umfang="TN_P_MA_P"; foerder_umfang="TN_P_MA_P_REF");
  tn_aktiv; OR(tn_kreis; tn_pauschal);
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; lk_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; lk_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; lk_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(INDEX(active_rows;1;1)="LEER"; IF(debug_mode; "⚠️ Keine passenden Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht. Aktuell: " & event_tage; "");
        LET(
          col_lk; CHOOSECOLS(active_rows; 27);
          col_fn; CHOOSECOLS(active_rows; 2);
          
          age_ok; LAMBDA(a; fn; IF(OR(fn="MA"; fn="REF"); TRUE; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter))));
          
          all_tn_raw; IFERROR(FILTER(active_rows; col_fn="TN"); "");
          has_tn_raw; AND(INDEX(all_tn_raw;1;1)<>""; IFERROR(ROWS(all_tn_raw)>0; FALSE));
          
          all_tn_filtered_age; IF(NOT(has_tn_raw); ""; LET(tn_ages; CHOOSECOLS(all_tn_raw; 26); tn_fns; CHOOSECOLS(all_tn_raw; 2); tn_age_check; MAP(tn_ages; tn_fns; age_ok); filtered; IFERROR(FILTER(all_tn_raw; tn_age_check); ""); IF(INDEX(filtered;1;1)=""; ""; filtered)));
          
          all_ma_filtered; IFERROR(FILTER(active_rows; col_fn="MA"); "");
          has_ma_filtered; AND(INDEX(all_ma_filtered;1;1)<>""; IFERROR(ROWS(all_ma_filtered)>0; FALSE));
          
          all_ref_filtered; IFERROR(FILTER(active_rows; col_fn="REF"); "");
          has_ref_filtered; AND(INDEX(all_ref_filtered;1;1)<>""; IFERROR(ROWS(all_ref_filtered)>0; FALSE));
          
          tn_locals_cnt; LET(tn; all_tn_filtered_age; IF(INDEX(tn;1;1)=""; 0; COUNTIF(CHOOSECOLS(tn; 27); clean_landkreis)));
          all_tn_cnt; IF(INDEX(all_tn_filtered_age;1;1)=""; 0; ROWS(all_tn_filtered_age));
          tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
          local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
          quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
          
          tn_list_obj; LET(
             raw; all_tn_filtered_age;
             cnt; IF(INDEX(raw;1;1)=""; 0; ROWS(raw));
             lk_col; IF(cnt=0; ""; CHOOSECOLS(raw; 27));
             loc_cnt; IF(cnt=0; 0; COUNTIF(lk_col; clean_landkreis));
             loc_rows; IF(loc_cnt>0; FILTER(raw; lk_col=clean_landkreis); "");
             aus_rows; IF(cnt=0; ""; FILTER(raw; lk_col<>clean_landkreis));
             list; IF(NOT(tn_aktiv); ""; IF(cnt=0; ""; IF(AND(quote_erfuellt; logik_modus="Auffüllen"); raw; IF(loc_cnt>0; loc_rows; ""))));
             list
          );
          
          ma_list_obj; LET(
             raw; all_ma_filtered;
             cnt; IF(NOT(has_ma_filtered); 0; ROWS(raw));
             lk_col; IF(cnt=0; ""; CHOOSECOLS(raw; 27));
             loc_cnt; IF(cnt=0; 0; COUNTIF(lk_col; clean_landkreis));
             loc_rows; IF(loc_cnt>0; FILTER(raw; lk_col=clean_landkreis); "");
             list; IF(NOT(ma_aktiv); ""; IF(cnt=0; ""; IF(AND(quote_erfuellt; logik_modus="Auffüllen"); raw; IF(loc_cnt>0; loc_rows; ""))));
             list
          );
          
          ref_list_obj; IF(NOT(ref_aktiv); ""; all_ref_filtered);
          

          dataset_unordered; IF(target_type="TN"; tn_list_obj; IF(target_type="MA"; ma_list_obj; ref_list_obj));
          has_data; AND(INDEX(dataset_unordered;1;1)<>""; IFERROR(ROWS(dataset_unordered)>0; FALSE));
          
          dataset_sorted; IF(NOT(has_data); "";
            IF(OR(target_type="REF"; logik_modus<>"Auffüllen"); 
               SORT(dataset_unordered; 12; TRUE); 
               LET(
                 col_lk_final; CHOOSECOLS(dataset_unordered; 27);
                 lokale; IFERROR(FILTER(dataset_unordered; col_lk_final=clean_landkreis); "");
                 auswaertige; IFERROR(FILTER(dataset_unordered; col_lk_final<>clean_landkreis); "");
                 lokale_sorted; IF(INDEX(lokale;1;1)=""; lokale; SORT(lokale; 12; TRUE));
                 auswaertige_sorted; IF(INDEX(auswaertige;1;1)=""; auswaertige; SORT(auswaertige; 12; TRUE));
                 has_lok; AND(INDEX(lokale_sorted;1;1)<>""; IFERROR(ROWS(lokale_sorted)>0; FALSE));
                 has_aus; AND(INDEX(auswaertige_sorted;1;1)<>""; IFERROR(ROWS(auswaertige_sorted)>0; FALSE));
                 IF(has_lok; IF(has_aus; VSTACK(lokale_sorted; auswaertige_sorted); lokale_sorted); IF(has_aus; auswaertige_sorted; ""))
               )
            )
          );
          
          cnt_final; IF(INDEX(dataset_sorted;1;1)=""; 0; ROWS(dataset_sorted));

          IF(start_idx > cnt_final; "";
            LET(
              actual_end; MIN(end_idx; cnt_final);
              page_rows; actual_end - start_idx + 1;
              
              page_data; CHOOSEROWS(dataset_sorted; SEQUENCE(page_rows; 1; start_idx));
              
              col_name; MAP(CHOOSECOLS(page_data; 13); CHOOSECOLS(page_data; 12); LAMBDA(v;n; v & " " & n));
              col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & " " & ort));
              col_datum; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "dd.MM.yyyy")));
              col_tage; CHOOSECOLS(page_data; 6);
              col_uebernachtungen; MAP(col_tage; LAMBDA(t; IF(ISNUMBER(t); t-1; 0)));
              col_leer; MAP(SEQUENCE(page_rows); LAMBDA(x; ""));
              
              IF(target_type="REF";
                 HSTACK(col_name; col_plz_ort; col_leer; col_leer; col_leer);
                 HSTACK(col_name; col_plz_ort; col_datum; col_tage; col_uebernachtungen; col_leer)
              )
            )
          )
        )
      )
    )
  )
)
```

---

## Teil 2 – TN Liste Fortsetzung (Zelle B28)

> Änderugen: `target_type; "TN"`, `page_size; 10`, `start_offset; 22`

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  target_type; "TN";
  page_size; 10;
  start_offset; 22;
  ... (Rest identisch zu Teil 1)
```

---

## Teil 3 – MA Liste (Zelle B40)

> Änderungen: `target_type; "MA"`, `page_size; 6`, `start_offset; 0`

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  target_type; "MA";
  page_size; 6;
  start_offset; 0;
  ... (Rest identisch zu Teil 1)
```

---

## Teil 4 – REF Liste (Zelle B49)

> Änderungen: `target_type; "REF"`, `page_size; 2`, `start_offset; 0`

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  target_type; "REF";
  page_size; 2;
  start_offset; 0;
  ... (Rest identisch zu Teil 1)
```
