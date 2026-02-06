# Formel für Westerwaldkreis V6

**Status:** ✅ v6 – 4-Seiten-Layout mit wiederholenden Headern  
**Kürzel:** WW

## Layout-Übersicht

Da die Header sich auf jeder Seite wiederholen, werden **4 separate Formeln** verwendet:

| Seite | Formel-Zelle | Daten-Bereich | Zeilen der Daten |
|-------|--------------|---------------|------------------|
| 1 | **B4** | B4:F23 | 1-20 |
| 2 | **B27** | B27:F46 | 21-40 |
| 3 | **B50** | B50:F69 | 41-60 |
| 4 | **B73** | B73:F92 | 61-80 |

> **Betreuer-Zählung** (ehrenamtlich/hauptamtlich) wird händisch in Zeilen 2, 25, 48, 71 eingetragen.

---

## Output-Spalten

| Spalte | Feld | Quelle |
|--------|------|--------|
| A | Lfd. Nr | *separat* |
| B | Name, Vorname | Index 12 + 13 |
| C | PLZ, Wohnort | Index 16 + 17 |
| D | Geburts-Jahr | YEAR(Index 14) |
| E | TN-Tage | Index 6 (Anwesenheit) |
| F | Vollständige Unterschrift | leer (manuell) |

---

## CACHE_RULES Keys

| Key | Event-Typ |
|-----|-----------|
| `Landkreis Westerwaldkreis_Soziale_Bildung` | Soziale_Bildung |
| `Landkreis Westerwaldkreis_Schulung_Ehrenamtlicher_Mitarbeitenden` | Schulung |
| `Landkreis Westerwaldkreis_Politische_Jugendbildung` | Politische_Jugendbildung |

---

## Seite 1 – Zelle B4 (Zeilen 1-20)

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  page; 1;
  page_size; 20;
  start_idx; (page - 1) * page_size + 1;
  end_idx; page * page_size;
  
  ziel_landkreis; "Landkreis Westerwaldkreis";
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
          
          all_tn; IF(NOT(has_tn_raw); ""; LET(tn_ages; CHOOSECOLS(all_tn_raw; 26); tn_fns; CHOOSECOLS(all_tn_raw; 2); tn_age_check; MAP(tn_ages; tn_fns; age_ok); filtered; IFERROR(FILTER(all_tn_raw; tn_age_check); ""); IF(INDEX(filtered;1;1)=""; ""; filtered)));
          
          all_ma; IFERROR(FILTER(active_rows; col_fn="MA"); "");
          has_ma_raw; AND(INDEX(all_ma;1;1)<>""; IFERROR(ROWS(all_ma)>0; FALSE));
          
          all_ref; IFERROR(FILTER(active_rows; col_fn="REF"); "");
          has_ref_raw; AND(INDEX(all_ref;1;1)<>""; IFERROR(ROWS(all_ref)>0; FALSE));
          
          all_tn_cnt; IF(INDEX(all_tn;1;1)=""; 0; ROWS(all_tn));
          all_ma_cnt; IF(NOT(has_ma_raw); 0; ROWS(all_ma));
          all_ref_cnt; IF(NOT(has_ref_raw); 0; ROWS(all_ref));
          
          tn_lk; IF(all_tn_cnt=0; ""; CHOOSECOLS(all_tn; 27));
          tn_locals_cnt; IF(all_tn_cnt=0; 0; COUNTIF(tn_lk; clean_landkreis));
          tn_locals; IF(tn_locals_cnt>0; FILTER(all_tn; tn_lk=clean_landkreis); "");
          
          local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
          tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
          quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
          use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
          
          final_tn; IF(NOT(tn_aktiv); ""; IF(all_tn_cnt=0; ""; IF(use_all; all_tn; IF(tn_locals_cnt>0; tn_locals; ""))));
          
          ma_lk; IF(all_ma_cnt=0; ""; CHOOSECOLS(all_ma; 27));
          ma_locals_cnt; IF(all_ma_cnt=0; 0; COUNTIF(ma_lk; clean_landkreis));
          ma_locals; IF(ma_locals_cnt>0; FILTER(all_ma; ma_lk=clean_landkreis); "");
          
          final_ma; IF(NOT(ma_aktiv); ""; IF(all_ma_cnt=0; ""; IF(use_all; all_ma; IF(ma_locals_cnt>0; ma_locals; ""))));
          
          final_ref; IF(NOT(ref_aktiv); ""; IF(all_ref_cnt=0; ""; all_ref));
          
          has_final_tn; AND(INDEX(final_tn;1;1)<>""; IFERROR(ROWS(final_tn)>0; FALSE));
          has_final_ma; AND(INDEX(final_ma;1;1)<>""; IFERROR(ROWS(final_ma)>0; FALSE));
          has_final_ref; AND(INDEX(final_ref;1;1)<>""; IFERROR(ROWS(final_ref)>0; FALSE));
          
          final_list; LET(
            tn_ma; IF(has_final_tn; IF(has_final_ma; VSTACK(final_tn; final_ma); final_tn); IF(has_final_ma; final_ma; ""));
            has_tn_ma; AND(INDEX(tn_ma;1;1)<>""; IFERROR(ROWS(tn_ma)>0; FALSE));
            IF(has_tn_ma; IF(has_final_ref; VSTACK(tn_ma; final_ref); tn_ma); IF(has_final_ref; final_ref; "LEER"))
          );
          
          final_list_sorted; IF(INDEX(final_list;1;1)="LEER"; final_list;
            LET(
              col_lk_final; CHOOSECOLS(final_list; 27);
              lokale; IFERROR(FILTER(final_list; col_lk_final=clean_landkreis); "");
              auswaertige; IFERROR(FILTER(final_list; col_lk_final<>clean_landkreis); "");
              lokale_sorted; IF(INDEX(lokale;1;1)=""; lokale; SORT(lokale; 12; TRUE));
              auswaertige_sorted; IF(INDEX(auswaertige;1;1)=""; auswaertige; SORT(auswaertige; 12; TRUE));
              has_lok; AND(INDEX(lokale_sorted;1;1)<>""; IFERROR(ROWS(lokale_sorted)>0; FALSE));
              has_aus; AND(INDEX(auswaertige_sorted;1;1)<>""; IFERROR(ROWS(auswaertige_sorted)>0; FALSE));
              IF(has_lok; IF(has_aus; VSTACK(lokale_sorted; auswaertige_sorted); lokale_sorted); IF(has_aus; auswaertige_sorted; "LEER"))
            )
          );
          
          cnt_final; IF(INDEX(final_list_sorted;1;1)="LEER"; 0; ROWS(final_list_sorted));
          
          IF(AND(page = 1; cnt_final = 0); IF(debug_mode; "⚠️ Keine Personen nach Filter"; "");
            IF(AND(page = 1; cnt_final < min_tn); IF(debug_mode; "⚠️ Min TN (" & min_tn & ") nicht erreicht. Aktuell: " & cnt_final; "");
              IF(start_idx > cnt_final; "";
                LET(
                  actual_end; MIN(end_idx; cnt_final);
                  page_rows; actual_end - start_idx + 1;
                  
                  page_data; CHOOSEROWS(final_list_sorted; SEQUENCE(page_rows; 1; start_idx));
                  
                  col_name; MAP(CHOOSECOLS(page_data; 12); CHOOSECOLS(page_data; 13); LAMBDA(n;v; n & ", " & v));
                  col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & ", " & ort));
                  col_jahr; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "yyyy")));
                  col_tage; CHOOSECOLS(page_data; 6);
                  col_leer; MAP(SEQUENCE(page_rows); LAMBDA(x; ""));
                  
                  HSTACK(col_name; col_plz_ort; col_jahr; col_tage; col_leer)
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

## Seite 2 – Zelle B27 (Zeilen 21-40)

> **Nur die erste Zeile ändern:** `page; 2;`

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  page; 2;
  page_size; 20;
  start_idx; (page - 1) * page_size + 1;
  end_idx; page * page_size;
  
  ziel_landkreis; "Landkreis Westerwaldkreis";
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
  
  IF(rule_check="NOT_FOUND"; "";
    IF(INDEX(active_rows;1;1)="LEER"; "";
      IF(AND(min_tage > 0; event_tage < min_tage); "";
        LET(
          col_lk; CHOOSECOLS(active_rows; 27);
          col_fn; CHOOSECOLS(active_rows; 2);
          
          age_ok; LAMBDA(a; fn; IF(OR(fn="MA"; fn="REF"); TRUE; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter))));
          
          all_tn_raw; IFERROR(FILTER(active_rows; col_fn="TN"); "");
          has_tn_raw; AND(INDEX(all_tn_raw;1;1)<>""; IFERROR(ROWS(all_tn_raw)>0; FALSE));
          
          all_tn; IF(NOT(has_tn_raw); ""; LET(tn_ages; CHOOSECOLS(all_tn_raw; 26); tn_fns; CHOOSECOLS(all_tn_raw; 2); tn_age_check; MAP(tn_ages; tn_fns; age_ok); filtered; IFERROR(FILTER(all_tn_raw; tn_age_check); ""); IF(INDEX(filtered;1;1)=""; ""; filtered)));
          
          all_ma; IFERROR(FILTER(active_rows; col_fn="MA"); "");
          has_ma_raw; AND(INDEX(all_ma;1;1)<>""; IFERROR(ROWS(all_ma)>0; FALSE));
          
          all_ref; IFERROR(FILTER(active_rows; col_fn="REF"); "");
          has_ref_raw; AND(INDEX(all_ref;1;1)<>""; IFERROR(ROWS(all_ref)>0; FALSE));
          
          all_tn_cnt; IF(INDEX(all_tn;1;1)=""; 0; ROWS(all_tn));
          all_ma_cnt; IF(NOT(has_ma_raw); 0; ROWS(all_ma));
          all_ref_cnt; IF(NOT(has_ref_raw); 0; ROWS(all_ref));
          
          tn_lk; IF(all_tn_cnt=0; ""; CHOOSECOLS(all_tn; 27));
          tn_locals_cnt; IF(all_tn_cnt=0; 0; COUNTIF(tn_lk; clean_landkreis));
          tn_locals; IF(tn_locals_cnt>0; FILTER(all_tn; tn_lk=clean_landkreis); "");
          
          local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
          tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
          quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
          use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
          
          final_tn; IF(NOT(tn_aktiv); ""; IF(all_tn_cnt=0; ""; IF(use_all; all_tn; IF(tn_locals_cnt>0; tn_locals; ""))));
          
          ma_lk; IF(all_ma_cnt=0; ""; CHOOSECOLS(all_ma; 27));
          ma_locals_cnt; IF(all_ma_cnt=0; 0; COUNTIF(ma_lk; clean_landkreis));
          ma_locals; IF(ma_locals_cnt>0; FILTER(all_ma; ma_lk=clean_landkreis); "");
          
          final_ma; IF(NOT(ma_aktiv); ""; IF(all_ma_cnt=0; ""; IF(use_all; all_ma; IF(ma_locals_cnt>0; ma_locals; ""))));
          
          final_ref; IF(NOT(ref_aktiv); ""; IF(all_ref_cnt=0; ""; all_ref));
          
          has_final_tn; AND(INDEX(final_tn;1;1)<>""; IFERROR(ROWS(final_tn)>0; FALSE));
          has_final_ma; AND(INDEX(final_ma;1;1)<>""; IFERROR(ROWS(final_ma)>0; FALSE));
          has_final_ref; AND(INDEX(final_ref;1;1)<>""; IFERROR(ROWS(final_ref)>0; FALSE));
          
          final_list; LET(
            tn_ma; IF(has_final_tn; IF(has_final_ma; VSTACK(final_tn; final_ma); final_tn); IF(has_final_ma; final_ma; ""));
            has_tn_ma; AND(INDEX(tn_ma;1;1)<>""; IFERROR(ROWS(tn_ma)>0; FALSE));
            IF(has_tn_ma; IF(has_final_ref; VSTACK(tn_ma; final_ref); tn_ma); IF(has_final_ref; final_ref; "LEER"))
          );
          
          final_list_sorted; IF(INDEX(final_list;1;1)="LEER"; final_list;
            LET(
              col_lk_final; CHOOSECOLS(final_list; 27);
              lokale; IFERROR(FILTER(final_list; col_lk_final=clean_landkreis); "");
              auswaertige; IFERROR(FILTER(final_list; col_lk_final<>clean_landkreis); "");
              lokale_sorted; IF(INDEX(lokale;1;1)=""; lokale; SORT(lokale; 12; TRUE));
              auswaertige_sorted; IF(INDEX(auswaertige;1;1)=""; auswaertige; SORT(auswaertige; 12; TRUE));
              has_lok; AND(INDEX(lokale_sorted;1;1)<>""; IFERROR(ROWS(lokale_sorted)>0; FALSE));
              has_aus; AND(INDEX(auswaertige_sorted;1;1)<>""; IFERROR(ROWS(auswaertige_sorted)>0; FALSE));
              IF(has_lok; IF(has_aus; VSTACK(lokale_sorted; auswaertige_sorted); lokale_sorted); IF(has_aus; auswaertige_sorted; "LEER"))
            )
          );
          
          cnt_final; IF(INDEX(final_list_sorted;1;1)="LEER"; 0; ROWS(final_list_sorted));
          
          IF(start_idx > cnt_final; "";
            LET(
              actual_end; MIN(end_idx; cnt_final);
              page_rows; actual_end - start_idx + 1;
              
              page_data; CHOOSEROWS(final_list_sorted; SEQUENCE(page_rows; 1; start_idx));
              
              col_name; MAP(CHOOSECOLS(page_data; 12); CHOOSECOLS(page_data; 13); LAMBDA(n;v; n & ", " & v));
              col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & ", " & ort));
              col_jahr; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "yyyy")));
              col_tage; CHOOSECOLS(page_data; 6);
              col_leer; MAP(SEQUENCE(page_rows); LAMBDA(x; ""));
              
              HSTACK(col_name; col_plz_ort; col_jahr; col_tage; col_leer)
            )
          )
        )
      )
    )
  )
)
```

---

## Seite 3 – Zelle B50 (Zeilen 41-60)

> **Nur die erste Zeile ändern:** `page; 3;`

*(Gleiche Formel wie Seite 2, aber mit `page; 3;`)*

---

## Seite 4 – Zelle B73 (Zeilen 61-80)

> **Nur die erste Zeile ändern:** `page; 4;`

*(Gleiche Formel wie Seite 2, aber mit `page; 4;`)*

---

## Änderungshistorie

**V6.3 (2026-01-21):**
- DEBUG_MODUS hinzugefügt: `SETUP!B69` = "Ja"/"Nein"
- Alle Fehlermeldungen werden nur bei debug_mode=TRUE angezeigt

**V6.2 (2026-01-20):**
- 4-Seiten-Layout implementiert
- Separate Formeln pro Seite (page 1-4)
- Wiederholende Header werden nicht mehr überschrieben
- Fehlermeldungen nur auf Seite 1, Seiten 2-4 zeigen leer wenn keine Daten

**V6.1 (2026-01-20):**
- Gap-Logik mit MAKEARRAY (verworfen wegen Header-Konflikt)

**V6 (2026-01-20):**
- Initiale V6 für Westerwaldkreis
- 5-Spalten Output: Name+Vorname, PLZ+Wohnort, Geburtsjahr, TN-Tage, Unterschrift
- 12 Förderumfang-Codes mit REF
- Sortierung: Lokal zuerst, dann alphabetisch
