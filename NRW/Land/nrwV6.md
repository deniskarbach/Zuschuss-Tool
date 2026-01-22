# Formel für Landesliste NRW V6

**Status:** ✅ v6 – Mixed List (TN, MA, REF, LEITUNG) mit speziellem Paging  
**Kürzel:** NRW

## Layout-Übersicht

Die Liste hat **2 Formel-Blöcke** mit unterschiedlicher Kapazität:

| Bereich | Zelle | Zeilen | Kapazität | Seite |
|---------|-------|--------|-----------|-------|
| 1 | **B8** | 8-21 | 14 | 1 |
| 2 | **B32** | 32-145 | 114 | 2+ |

---

## Output-Spalten

| Spalte | Header | Feld | Logik |
|--------|--------|------|-------|
| B | Name | Name | `Name` (Index 12) |
| C | Vorname | Vorname | `Vorname` (Index 13) |
| D | L / M | Funktion | "L" (Leitung) / "M" (Mitarbeiter) |
| E | Alter | Alter | `Alter` (Index 26) |
| F | PLZ | PLZ | `PLZ` (Index 16) |
| G | Wohnort | Wohnort | `Wohnort` (Index 17) |
| H | Straße | Straße | `Straße` (Index 15) |

---

## CACHE_RULES Keys

| Key | Event-Typ | Region |
|-----|-----------|--------|
| `Nordrhein-Westfalen_Soziale_Bildung` | Soziale_Bildung | NRW |
| `Nordrhein-Westfalen_Schulung_Ehrenamtlicher_Mitarbeitenden` | Schulung | NRW |
| `Nordrhein-Westfalen_Politische_Jugendbildung` | Politische_Jugendbildung | NRW |

---

## Bereich 1: Seite 1 – Zelle B8 (14 Zeilen)

```excel
=LET(
  start_idx; 1;
  max_rows; 14;
  debug_mode; SETUP!B69="Ja";
  
  ziel_region; "Nordrhein-Westfalen";
  event_typ_raw; SETUP!B18;
  event_start; SETUP!B23;
  event_ende; SETUP!H23;
  cache_rules; CACHE_RULES!A:Z;
  
  clean_region; TRIM(CLEAN(ziel_region));
  clean_event; SUBSTITUTE(TRIM(CLEAN(event_typ_raw)); " "; "_");
  rule_key; clean_region & "_" & clean_event;
  
  get_rule; LAMBDA(col; IFERROR(VLOOKUP(rule_key; cache_rules; col; 0); "NOT_FOUND"));
  rule_check; get_rule(1);
  
  check_local; LAMBDA(r; OR(TRIM(CLEAN(r))=clean_region; TRIM(CLEAN(r))="NRW"));
  
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
  
  event_tage; LET(
    start_num; IF(ISNUMBER(event_start); event_start; IFERROR(DATEVALUE(event_start); 0));
    ende_num; IF(ISNUMBER(event_ende); event_ende; IFERROR(DATEVALUE(event_ende); 0));
    IF(AND(start_num > 0; ende_num > 0); ende_num - start_num + 1; 0)
  );

  tn_kreis; OR(foerder_umfang="TN_K"; foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF");
  tn_pauschal; OR(foerder_umfang="TN_P"; foerder_umfang="TN_P_MA_K"; foerder_umfang="TN_P_MA_P"; foerder_umfang="TN_P_MA_P_REF");
  tn_aktiv; OR(tn_kreis; tn_pauschal);
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");

  raw_data; TN_LISTE!B3:AC1710;
  status_col; CHOOSECOLS(raw_data; 1);
  geo_col; CHOOSECOLS(raw_data; 28); 
  
  filtered_data; IFERROR(FILTER(raw_data; status_col="Angemeldet"; geo_col<>""); "");
  has_data; IFERROR(COLUMNS(filtered_data)>1; FALSE);

  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(NOT(has_data); IF(debug_mode; "⚠️ Keine Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht"; "");
        LET(
          col_fn; CHOOSECOLS(filtered_data; 2);
          col_age; CHOOSECOLS(filtered_data; 26);
          col_geo; CHOOSECOLS(filtered_data; 27); 

          age_ok; LAMBDA(a; fn; IF(OR(fn="MA"; fn="REF"; fn="LEITUNG"); TRUE; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter))));
          row_check; MAP(col_age; col_fn; age_ok);
          
          valid_data; IFERROR(FILTER(filtered_data; row_check); "");
          has_valid; IFERROR(COLUMNS(valid_data)>1; FALSE);
          
          IF(NOT(has_valid); IF(debug_mode; "⚠️ Keine Personen nach Altersfilter"; "");
            LET(
              fn_valid; CHOOSECOLS(valid_data; 2);
              
              all_tn; IFERROR(FILTER(valid_data; fn_valid="TN"); "");
              has_tn; IFERROR(COLUMNS(all_tn)>1; FALSE);
              
              all_ma; IFERROR(FILTER(valid_data; fn_valid="MA"); "");
              has_ma; IFERROR(COLUMNS(all_ma)>1; FALSE);
              
              all_ref; IFERROR(FILTER(valid_data; fn_valid="REF"); "");
              has_ref; IFERROR(COLUMNS(all_ref)>1; FALSE);
              
              all_leitung; IFERROR(FILTER(valid_data; fn_valid="LEITUNG"); "");
              has_leitung; IFERROR(COLUMNS(all_leitung)>1; FALSE);

              tn_cnt; IF(has_tn; ROWS(all_tn); 0);
              ma_cnt; IF(has_ma; ROWS(all_ma); 0);
              ref_cnt; IF(has_ref; ROWS(all_ref); 0);
              leitung_cnt; IF(has_leitung; ROWS(all_leitung); 0);
              
              tn_locals_cnt; IF(has_tn; SUM(MAP(CHOOSECOLS(all_tn; 28); check_local)); 0);
              tn_loc_percent; IF(tn_cnt>0; tn_locals_cnt/tn_cnt; 0);
              tn_aus_cnt; tn_cnt - tn_locals_cnt;
              
              quote_ok; IF(min_quote=0; TRUE; IF(quote_modus="PROZENT"; tn_loc_percent>=min_quote; tn_locals_cnt>tn_aus_cnt));
              use_all; AND(quote_ok; logik_modus="Auffüllen");
              
              final_tn; IF(NOT(tn_aktiv); ""; IF(NOT(has_tn); ""; IF(tn_pauschal; all_tn; IF(use_all; all_tn; IFERROR(FILTER(all_tn; MAP(CHOOSECOLS(all_tn; 28); check_local)); "")))));
              
              ma_locals_cnt; IF(has_ma; SUM(MAP(CHOOSECOLS(all_ma; 28); check_local)); 0);
              final_ma; IF(NOT(ma_aktiv); ""; IF(NOT(has_ma); ""; IF(ma_pauschal; all_ma; IF(use_all; all_ma; IFERROR(FILTER(all_ma; MAP(CHOOSECOLS(all_ma; 28); check_local)); "")))));

              final_ref_list; IF(NOT(ref_aktiv); ""; IF(NOT(has_ref); ""; all_ref));

              final_leit_list; IF(NOT(has_leitung); ""; all_leitung); 
              
              stack1; IF(INDEX(final_leit_list;1;1)=""; ""; final_leit_list);
              stack2; IF(INDEX(final_ref_list;1;1)=""; stack1; IF(stack1=""; final_ref_list; VSTACK(stack1; final_ref_list)));
              stack3; IF(INDEX(final_ma;1;1)=""; stack2; IF(stack2=""; final_ma; VSTACK(stack2; final_ma)));
              stack4; IF(INDEX(final_tn;1;1)=""; stack3; IF(stack3=""; final_tn; VSTACK(stack3; final_tn)));
              
              result_list; IF(quote_ok; stack4; "");
              has_result; IFERROR(COLUMNS(result_list)>1; FALSE);
              
              IF(NOT(has_result); IF(debug_mode; "⚠️ Keine Personen nach Quote/Filter"; "");
                LET(
                   geo_final; CHOOSECOLS(result_list; 28);
                   is_local; MAP(geo_final; check_local);
                   
                   p_local; IFERROR(FILTER(result_list; is_local); "");
                   p_foreign; IFERROR(FILTER(result_list; NOT(is_local)); "");
                   
                   p_local_sorted; IF(INDEX(p_local;1;1)=""; ""; SORT(p_local; 12; TRUE));
                   p_foreign_sorted; IF(INDEX(p_foreign;1;1)=""; ""; SORT(p_foreign; 12; TRUE));
                   
                   final_sorted; IF(INDEX(p_local_sorted;1;1)=""; p_foreign_sorted; IF(INDEX(p_foreign_sorted;1;1)=""; p_local_sorted; VSTACK(p_local_sorted; p_foreign_sorted)));
                   
                   cnt_final; IF(IFERROR(COLUMNS(final_sorted)>1; FALSE); ROWS(final_sorted); 0);
                   
                   IF(start_idx > cnt_final; "";
                     LET(
                       actual_end; MIN(start_idx + max_rows - 1; cnt_final);
                       page_rows; actual_end - start_idx + 1;
                       page_data; CHOOSEROWS(final_sorted; SEQUENCE(page_rows; 1; start_idx));
                       
                       c_name; CHOOSECOLS(page_data; 12);
                       c_vorname; CHOOSECOLS(page_data; 13);
                       c_func; CHOOSECOLS(page_data; 2);
                       c_lm; MAP(c_func; LAMBDA(f; IF(f="LEITUNG"; "L"; IF(f="MA"; "M"; ""))));
                       c_alter; CHOOSECOLS(page_data; 26);
                       c_plz; CHOOSECOLS(page_data; 16);
                       c_ort; CHOOSECOLS(page_data; 17);
                       c_str; CHOOSECOLS(page_data; 15);
                       
                       HSTACK(c_name; c_vorname; c_lm; c_alter; c_plz; c_ort; c_str)
                     )
                   )
                )
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

## Bereich 2: Seite 2+ – Zelle B32 (114 Zeilen)

> **Nur die Parameter ändern:**
> `start_idx; 15;`
> `max_rows; 114;`

```excel
=LET(
  start_idx; 15;
  max_rows; 114;
  debug_mode; SETUP!B69="Ja";
  
  ziel_region; "Nordrhein-Westfalen";
  event_typ_raw; SETUP!B18;
  event_start; SETUP!B23;
  event_ende; SETUP!H23;
  cache_rules; CACHE_RULES!A:Z;
  
  clean_region; TRIM(CLEAN(ziel_region));
  clean_event; SUBSTITUTE(TRIM(CLEAN(event_typ_raw)); " "; "_");
  rule_key; clean_region & "_" & clean_event;
  
  get_rule; LAMBDA(col; IFERROR(VLOOKUP(rule_key; cache_rules; col; 0); "NOT_FOUND"));
  rule_check; get_rule(1);
  
  check_local; LAMBDA(r; OR(TRIM(CLEAN(r))=clean_region; TRIM(CLEAN(r))="NRW"));
  
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
  
  event_tage; LET(
    start_num; IF(ISNUMBER(event_start); event_start; IFERROR(DATEVALUE(event_start); 0));
    ende_num; IF(ISNUMBER(event_ende); event_ende; IFERROR(DATEVALUE(event_ende); 0));
    IF(AND(start_num > 0; ende_num > 0); ende_num - start_num + 1; 0)
  );

  tn_kreis; OR(foerder_umfang="TN_K"; foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF");
  tn_pauschal; OR(foerder_umfang="TN_P"; foerder_umfang="TN_P_MA_K"; foerder_umfang="TN_P_MA_P"; foerder_umfang="TN_P_MA_P_REF");
  tn_aktiv; OR(tn_kreis; tn_pauschal);
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");

  raw_data; TN_LISTE!B3:AC1710;
  status_col; CHOOSECOLS(raw_data; 1);
  geo_col; CHOOSECOLS(raw_data; 28); 
  
  filtered_data; IFERROR(FILTER(raw_data; status_col="Angemeldet"; geo_col<>""); "");
  has_data; IFERROR(COLUMNS(filtered_data)>1; FALSE);

  IF(rule_check="NOT_FOUND"; "";
    IF(NOT(has_data); "";
      IF(AND(min_tage > 0; event_tage < min_tage); "";
        LET(
          col_fn; CHOOSECOLS(filtered_data; 2);
          col_age; CHOOSECOLS(filtered_data; 26);
          col_geo; CHOOSECOLS(filtered_data; 27); 

          age_ok; LAMBDA(a; fn; IF(OR(fn="MA"; fn="REF"; fn="LEITUNG"); TRUE; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter))));
          row_check; MAP(col_age; col_fn; age_ok);
          
          valid_data; IFERROR(FILTER(filtered_data; row_check); "");
          has_valid; IFERROR(COLUMNS(valid_data)>1; FALSE);
          
          IF(NOT(has_valid); "";
            LET(
              fn_valid; CHOOSECOLS(valid_data; 2);
              
              all_tn; IFERROR(FILTER(valid_data; fn_valid="TN"); "");
              has_tn; IFERROR(COLUMNS(all_tn)>1; FALSE);
              
              all_ma; IFERROR(FILTER(valid_data; fn_valid="MA"); "");
              has_ma; IFERROR(COLUMNS(all_ma)>1; FALSE);
              
              all_ref; IFERROR(FILTER(valid_data; fn_valid="REF"); "");
              has_ref; IFERROR(COLUMNS(all_ref)>1; FALSE);
              
              all_leitung; IFERROR(FILTER(valid_data; fn_valid="LEITUNG"); "");
              has_leitung; IFERROR(COLUMNS(all_leitung)>1; FALSE);

              tn_cnt; IF(has_tn; ROWS(all_tn); 0);
              ma_cnt; IF(has_ma; ROWS(all_ma); 0);
              ref_cnt; IF(has_ref; ROWS(all_ref); 0);
              leitung_cnt; IF(has_leitung; ROWS(all_leitung); 0);
              
              tn_locals_cnt; IF(has_tn; SUM(MAP(CHOOSECOLS(all_tn; 28); check_local)); 0);
              tn_loc_percent; IF(tn_cnt>0; tn_locals_cnt/tn_cnt; 0);
              tn_aus_cnt; tn_cnt - tn_locals_cnt;
              
              quote_ok; IF(min_quote=0; TRUE; IF(quote_modus="PROZENT"; tn_loc_percent>=min_quote; tn_locals_cnt>tn_aus_cnt));
              use_all; AND(quote_ok; logik_modus="Auffüllen");
              
              final_tn; IF(NOT(tn_aktiv); ""; IF(NOT(has_tn); ""; IF(tn_pauschal; all_tn; IF(use_all; all_tn; IFERROR(FILTER(all_tn; MAP(CHOOSECOLS(all_tn; 28); check_local)); "")))));
              
              ma_locals_cnt; IF(has_ma; SUM(MAP(CHOOSECOLS(all_ma; 28); check_local)); 0);
              final_ma; IF(NOT(ma_aktiv); ""; IF(NOT(has_ma); ""; IF(ma_pauschal; all_ma; IF(use_all; all_ma; IFERROR(FILTER(all_ma; MAP(CHOOSECOLS(all_ma; 28); check_local)); "")))));

              final_ref_list; IF(NOT(ref_aktiv); ""; IF(NOT(has_ref); ""; all_ref));

              final_leit_list; IF(NOT(has_leitung); ""; all_leitung); 
              
              stack1; IF(INDEX(final_leit_list;1;1)=""; ""; final_leit_list);
              stack2; IF(INDEX(final_ref_list;1;1)=""; stack1; IF(stack1=""; final_ref_list; VSTACK(stack1; final_ref_list)));
              stack3; IF(INDEX(final_ma;1;1)=""; stack2; IF(stack2=""; final_ma; VSTACK(stack2; final_ma)));
              stack4; IF(INDEX(final_tn;1;1)=""; stack3; IF(stack3=""; final_tn; VSTACK(stack3; final_tn)));
              
              result_list; IF(quote_ok; stack4; "");
              has_result; IFERROR(COLUMNS(result_list)>1; FALSE);
              
              IF(NOT(has_result); "";
                LET(
                   geo_final; CHOOSECOLS(result_list; 28);
                   is_local; MAP(geo_final; check_local);
                   
                   p_local; IFERROR(FILTER(result_list; is_local); "");
                   p_foreign; IFERROR(FILTER(result_list; NOT(is_local)); "");
                   
                   p_local_sorted; IF(INDEX(p_local;1;1)=""; ""; SORT(p_local; 12; TRUE));
                   p_foreign_sorted; IF(INDEX(p_foreign;1;1)=""; ""; SORT(p_foreign; 12; TRUE));
                   
                   final_sorted; IF(INDEX(p_local_sorted;1;1)=""; p_foreign_sorted; IF(INDEX(p_foreign_sorted;1;1)=""; p_local_sorted; VSTACK(p_local_sorted; p_foreign_sorted)));
                   
                   cnt_final; IF(IFERROR(COLUMNS(final_sorted)>1; FALSE); ROWS(final_sorted); 0);
                   
                   IF(start_idx > cnt_final; "";
                     LET(
                       actual_end; MIN(start_idx + max_rows - 1; cnt_final);
                       page_rows; actual_end - start_idx + 1;
                       page_data; CHOOSEROWS(final_sorted; SEQUENCE(page_rows; 1; start_idx));
                       
                       c_name; CHOOSECOLS(page_data; 12);
                       c_vorname; CHOOSECOLS(page_data; 13);
                       c_func; CHOOSECOLS(page_data; 2);
                       c_lm; MAP(c_func; LAMBDA(f; IF(f="LEITUNG"; "L"; IF(f="MA"; "M"; ""))));
                       c_alter; CHOOSECOLS(page_data; 26);
                       c_plz; CHOOSECOLS(page_data; 16);
                       c_ort; CHOOSECOLS(page_data; 17);
                       c_str; CHOOSECOLS(page_data; 15);
                       
                       HSTACK(c_name; c_vorname; c_lm; c_alter; c_plz; c_ort; c_str)
                     )
                   )
                )
              )
            )
          )
        )
      )
    )
  )
)
```
