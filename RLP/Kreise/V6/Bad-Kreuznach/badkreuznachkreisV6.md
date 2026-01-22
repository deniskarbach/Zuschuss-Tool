# Formel für Bad Kreuznach V6

**Status:** ✅ v6 – 3 getrennte Bereiche (MA, REF, TN)  
**Kürzel:** KH-Kreis

## Layout-Übersicht

Die Liste hat **3 separate Bereiche** nach Funktion:

| Bereich | Funktion | Formel-Zelle | Datenzeilen | Kapazität |
|---------|----------|--------------|-------------|-----------|
| 1 | MA | **B4** | 4-15 | 12 |
| 2 | REF | **B20** | 20-24 | 5 |
| 3 | TN | **B29** | 29-177 | 149 |

---

## Output-Spalten

| Spalte | Feld | Quelle (Index) |
|--------|------|----------------|
| A | Lfd. Nr. | *separat* |
| B | Vor- und Zuname | 13 + 12 |
| C | PLZ | 16 |
| D | Wohnort | 17 |
| E | Geburtsjahr | YEAR(14) |
| F | Vereins-Tage | 6 |
| G | Unterschrift | leer |

---

## CACHE_RULES Keys

| Key | Event-Typ |
|-----|-----------|
| `Landkreis Bad Kreuznach_Soziale_Bildung` | Soziale_Bildung |
| `Landkreis Bad Kreuznach_Schulung_Ehrenamtlicher_Mitarbeitenden` | Schulung |
| `Landkreis Bad Kreuznach_Politische_Jugendbildung` | Politische_Jugendbildung |

---

## Bereich 1: MA – Zelle B4 (max 12 Zeilen)

```excel
=LET(
  bereich; "MA";
  max_rows; 12;
  debug_mode; SETUP!B69="Ja";
  
  ziel_landkreis; "Landkreis Bad Kreuznach";
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
  min_tage; LET(v; get_rule(10); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote_raw; LET(v; get_rule(11); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote; IF(min_quote_raw > 1; min_quote_raw / 100; min_quote_raw);
  quote_modus; LET(v; get_rule(12); IF(OR(v=""; v="--"; v="NOT_FOUND"); "MEHRHEIT"; UPPER(TRIM(v))));
  logik_modus; LET(v; get_rule(13); IF(OR(v=""; v="--"; v="NOT_FOUND"); "Standard"; TRIM(v)));
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; lk_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; lk_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; lk_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(INDEX(active_rows;1;1)="LEER"; IF(debug_mode; "⚠️ Keine Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht"; "");
        IF(NOT(ma_aktiv); "";
          LET(
            col_fn; CHOOSECOLS(active_rows; 2);
            col_lk; CHOOSECOLS(active_rows; 27);
            
            all_ma; IFERROR(FILTER(active_rows; col_fn="MA"); "");
            has_ma; AND(INDEX(all_ma;1;1)<>""; IFERROR(ROWS(all_ma)>0; FALSE));
            
            IF(NOT(has_ma); IF(debug_mode; "⚠️ Keine MA gefunden"; "");
              LET(
                all_ma_cnt; ROWS(all_ma);
                ma_lk; CHOOSECOLS(all_ma; 27);
                ma_locals_cnt; COUNTIF(ma_lk; clean_landkreis);
                ma_locals; IF(ma_locals_cnt>0; FILTER(all_ma; ma_lk=clean_landkreis); "");
                
                local_percent; IF(all_ma_cnt > 0; ma_locals_cnt / all_ma_cnt; 0);
                ma_auswaertige_cnt; all_ma_cnt - ma_locals_cnt;
                quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; ma_locals_cnt > ma_auswaertige_cnt));
                use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
                
                final_ma; IF(ma_pauschal; all_ma; IF(use_all; all_ma; IF(ma_locals_cnt>0; ma_locals; "")));
                has_final; AND(INDEX(final_ma;1;1)<>""; IFERROR(ROWS(final_ma)>0; FALSE));
                
                IF(NOT(has_final); IF(debug_mode; "⚠️ Keine MA nach Filter"; "");
                  LET(
                    sorted_ma; SORT(final_ma; 12; TRUE);
                    cnt; MIN(ROWS(sorted_ma); max_rows);
                    page_data; CHOOSEROWS(sorted_ma; SEQUENCE(cnt));
                    
                    col_name; MAP(CHOOSECOLS(page_data; 13); CHOOSECOLS(page_data; 12); LAMBDA(v;n; v & " " & n));
                    col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & ", " & ort));
                    col_jahr; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "yyyy")));
                    col_tage; CHOOSECOLS(page_data; 6);
                    col_leer; MAP(SEQUENCE(cnt); LAMBDA(x; ""));
                    
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
)
```

---

## Bereich 2: REF – Zelle B20 (max 5 Zeilen)

```excel
=LET(
  bereich; "REF";
  max_rows; 3;
  debug_mode; SETUP!B69="Ja";
  
  ziel_landkreis; "Landkreis Bad Kreuznach";
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
  min_tage; LET(v; get_rule(10); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; lk_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; lk_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; lk_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(INDEX(active_rows;1;1)="LEER"; IF(debug_mode; "⚠️ Keine Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer nicht erreicht"; "");
        IF(NOT(ref_aktiv); "";
          LET(
            col_fn; CHOOSECOLS(active_rows; 2);
            
            all_ref; IFERROR(FILTER(active_rows; col_fn="REF"); "");
            has_ref; AND(INDEX(all_ref;1;1)<>""; IFERROR(ROWS(all_ref)>0; FALSE));
            
            IF(NOT(has_ref); IF(debug_mode; "⚠️ Keine REF gefunden"; "");
              LET(
                sorted_ref; SORT(all_ref; 12; TRUE);
                cnt; MIN(ROWS(sorted_ref); max_rows);
                page_data; CHOOSEROWS(sorted_ref; SEQUENCE(cnt));
                
                col_name; MAP(CHOOSECOLS(page_data; 13); CHOOSECOLS(page_data; 12); LAMBDA(v;n; v & " " & n));
                col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & ", " & ort));
                col_jahr; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "yyyy")));
                col_tage; CHOOSECOLS(page_data; 6);
                col_leer; MAP(SEQUENCE(cnt); LAMBDA(x; ""));
                
                HSTACK(col_name; col_plz_ort; col_jahr; col_tage; col_leer)
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

## Bereich 3: TN – Zelle B29 (max 149 Zeilen)

```excel
=LET(
  bereich; "TN";
  max_rows; 149;
  debug_mode; SETUP!B69="Ja";
  
  ziel_landkreis; "Landkreis Bad Kreuznach";
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
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; lk_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; lk_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; lk_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(INDEX(active_rows;1;1)="LEER"; IF(debug_mode; "⚠️ Keine Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht"; "");
        IF(NOT(tn_aktiv); "";
          LET(
            col_fn; CHOOSECOLS(active_rows; 2);
            col_lk; CHOOSECOLS(active_rows; 27);
            
            age_ok; LAMBDA(a; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter)));
            
            all_tn_raw; IFERROR(FILTER(active_rows; col_fn="TN"); "");
            has_tn_raw; AND(INDEX(all_tn_raw;1;1)<>""; IFERROR(ROWS(all_tn_raw)>0; FALSE));
            
            IF(NOT(has_tn_raw); IF(debug_mode; "⚠️ Keine TN gefunden"; "");
              LET(
                tn_ages; CHOOSECOLS(all_tn_raw; 26);
                tn_age_check; MAP(tn_ages; age_ok);
                all_tn; IFERROR(FILTER(all_tn_raw; tn_age_check); "");
                has_tn; AND(INDEX(all_tn;1;1)<>""; IFERROR(ROWS(all_tn)>0; FALSE));
                
                IF(NOT(has_tn); IF(debug_mode; "⚠️ Keine TN im Altersbereich"; "");
                  LET(
                    all_tn_cnt; ROWS(all_tn);
                    tn_lk; CHOOSECOLS(all_tn; 27);
                    tn_locals_cnt; COUNTIF(tn_lk; clean_landkreis);
                    tn_locals; IF(tn_locals_cnt>0; FILTER(all_tn; tn_lk=clean_landkreis); "");
                    
                    local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
                    tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
                    quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
                    use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
                    
                    final_tn; IF(tn_pauschal; all_tn; IF(use_all; all_tn; IF(tn_locals_cnt>0; tn_locals; "")));
                    has_final; AND(INDEX(final_tn;1;1)<>""; IFERROR(ROWS(final_tn)>0; FALSE));
                    
                    IF(NOT(has_final); IF(debug_mode; "⚠️ Keine TN nach Filter"; "");
                      LET(
                        cnt_check; ROWS(final_tn);
                        IF(cnt_check < min_tn; IF(debug_mode; "⚠️ Min TN (" & min_tn & ") nicht erreicht. Aktuell: " & cnt_check; "");
                          LET(
                            col_lk_final; CHOOSECOLS(final_tn; 27);
                            lokale; IFERROR(FILTER(final_tn; col_lk_final=clean_landkreis); "");
                            auswaertige; IFERROR(FILTER(final_tn; col_lk_final<>clean_landkreis); "");
                            lokale_sorted; IF(INDEX(lokale;1;1)=""; lokale; SORT(lokale; 12; TRUE));
                            auswaertige_sorted; IF(INDEX(auswaertige;1;1)=""; auswaertige; SORT(auswaertige; 12; TRUE));
                            has_lok; AND(INDEX(lokale_sorted;1;1)<>""; IFERROR(ROWS(lokale_sorted)>0; FALSE));
                            has_aus; AND(INDEX(auswaertige_sorted;1;1)<>""; IFERROR(ROWS(auswaertige_sorted)>0; FALSE));
                            sorted_tn; IF(has_lok; IF(has_aus; VSTACK(lokale_sorted; auswaertige_sorted); lokale_sorted); IF(has_aus; auswaertige_sorted; ""));
                            
                            cnt; MIN(ROWS(sorted_tn); max_rows);
                            page_data; CHOOSEROWS(sorted_tn; SEQUENCE(cnt));
                            
                            col_name; MAP(CHOOSECOLS(page_data; 13); CHOOSECOLS(page_data; 12); LAMBDA(v;n; v & " " & n));
                            col_plz_ort; MAP(CHOOSECOLS(page_data; 16); CHOOSECOLS(page_data; 17); LAMBDA(plz;ort; plz & ", " & ort));
                            col_jahr; MAP(CHOOSECOLS(page_data; 14); LAMBDA(d; TEXT(d; "yyyy")));
                            col_tage; CHOOSECOLS(page_data; 6);
                            col_leer; MAP(SEQUENCE(cnt); LAMBDA(x; ""));
                            
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
        )
      )
    )
  )
)
```

---

## Änderungshistorie

**V6.1 (2026-01-21):**
- DEBUG_MODUS hinzugefügt: `SETUP!B69` = "Ja"/"Nein"
- Fehlermeldungen für MA und REF ergänzt (⚠️ Keine MA/REF gefunden/nach Filter)
- Alle Fehlermeldungen werden nur bei debug_mode=TRUE angezeigt
- Beim Drucken: B69 auf "Nein" setzen → leere Zellen statt Fehlermeldungen

**V6 (2026-01-20):**
- Initiale V6 für Bad Kreuznach
- 3 getrennte Bereiche nach Funktion (MA, REF, TN)
- 6-Spalten Output: Name, PLZ, Wohnort, Geburtsjahr, Tage, Unterschrift
- Fehlermeldungen in allen Bereichen
- 12 Förderumfang-Codes mit REF
- Sortierung: Lokal zuerst, dann alphabetisch (nur TN)
