# Master-Formel V6

**Status:** ✅ Unified Formula Foundation  
**Basis:** V6 (12 Förderumfang-Codes mit REF)

## Übersicht

Diese Master-Formel dient als **Grundlage für alle Zuschussformeln**. Sie ist durch CACHE_RULES Parameter vollständig konfigurierbar und unterstützt:

- **Geo-Level**: Landkreis oder Bundesland
- **Förderumfang**: 12 Codes (TN, MA, REF)
- **Quote**: PROZENT oder MEHRHEIT
- **Logik**: Standard oder Auffüllen
- **Sortierung**: Lokal zuerst, dann alphabetisch
- **Output**: Kreis-Format (4 Spalten) oder Land-Format (9 Spalten)

---

## Konfiguration über CACHE_RULES

| Spalte | Feld | Beschreibung |
|--------|------|--------------|
| E (5) | `FOERDER_UMFANG` | 12 Codes (TN_K, TN_P_MA_P_REF, etc.) |
| F (6) | `MIN_TN` | Mindestanzahl Teilnehmer |
| G (7) | `MIN_ALTER` | Hartes Mindestalter |
| H (8) | `MAX_ALTER` | Höchstalter |
| I (9) | `MIN_ALTER_SOFT` | Weiches Mindestalter |
| J (10) | `MIN_TAGE` | Mindest-Veranstaltungstage |
| K (11) | `Quote (%)` | Mindestanteil lokal |
| L (12) | `QUOTE_MODUS` | PROZENT / MEHRHEIT |
| M (13) | `Logik` | Standard / Auffüllen |
| N (14) | `GEO_LEVEL` | LANDKREIS / BUNDESLAND |
| O (15) | `OUTPUT_FORMAT` | KREIS / LAND |

---

## Förderumfang-Codes (12)

| Code | TN | MA | REF | Beschreibung |
|------|:--:|:--:|:---:|--------------|
| `TN_K` | K | — | — | Nur lokale TN |
| `TN_K_MA_K` | K | K | — | Lokale TN + MA |
| `TN_K_MA_P` | K | P | — | Lokale TN + alle MA |
| `TN_P` | P | — | — | Alle TN |
| `TN_P_MA_K` | P | K | — | Alle TN + lokale MA |
| `TN_P_MA_P` | P | P | — | Alle TN + alle MA |
| `MA_K` | — | K | — | Nur lokale MA |
| `MA_P` | — | P | — | Alle MA |
| `TN_K_REF` | K | — | P | Lokale TN + alle REF |
| `TN_K_MA_K_REF` | K | K | P | Lokale TN + MA + REF |
| `TN_P_MA_P_REF` | P | P | P | Alle TN + MA + REF |
| `REF` | — | — | P | Nur alle REF |

---

## Formel

```excel
=LET(
  event_typ_raw; SETUP!B18;
  event_start; SETUP!B23;
  event_ende; SETUP!H23;
  cache_rules; CACHE_RULES!A:Z;
  basis_landkreis; CACHE_RULES!B28;
  
  clean_event; SUBSTITUTE(TRIM(CLEAN(event_typ_raw)); " "; "_");
  
  lk_rule_key; TRIM(CLEAN(basis_landkreis)) & "_" & clean_event;
  geo_level_raw; LET(v; IFERROR(VLOOKUP(lk_rule_key; cache_rules; 14; 0); "NOT_FOUND"); IF(OR(v=""; v="--"; v="NOT_FOUND"); "LANDKREIS"; UPPER(TRIM(v))));
  is_land; geo_level_raw = "BUNDESLAND";
  
  ziel_geo; IF(is_land; "Rheinland-Pfalz"; basis_landkreis);
  clean_geo; TRIM(CLEAN(ziel_geo));
  rule_key; clean_geo & "_" & clean_event;
  
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
  
  geo_col_idx; IF(is_land; 28; 27);
  geo_z1; IF(is_land; TN_LISTE!AC3:AC749; TN_LISTE!AB3:AB749);
  geo_z2; IF(is_land; TN_LISTE!AC754:AC1454; TN_LISTE!AB754:AB1454);
  geo_z3; IF(is_land; TN_LISTE!AC1459:AC1710; TN_LISTE!AB1459:AB1710);
  
  get_rule; LAMBDA(col; IFERROR(VLOOKUP(rule_key; cache_rules; col; 0); "NOT_FOUND"));
  rule_check; get_rule(1);
  
  foerder_umfang; LET(v; get_rule(5); IF(OR(v=""; v="--"; v="NOT_FOUND"); IF(is_land; "TN_P_MA_P_REF"; "TN_K"); TRIM(v)));
  min_tn; LET(v; get_rule(6); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_alter; LET(v; get_rule(7); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  max_alter; LET(v; get_rule(8); IF(OR(v=""; v="--"; v="NOT_FOUND"); 999; VALUE(v)));
  min_alter_soft; LET(v; get_rule(9); IF(OR(v=""; v="--"; v="NOT_FOUND"); min_alter; VALUE(v)));
  min_tage; LET(v; get_rule(10); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote_raw; LET(v; get_rule(11); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote; IF(min_quote_raw > 1; min_quote_raw / 100; min_quote_raw);
  quote_modus; LET(v; get_rule(12); IF(OR(v=""; v="--"; v="NOT_FOUND"); IF(is_land; "PROZENT"; "MEHRHEIT"); UPPER(TRIM(v))));
  logik_modus; LET(v; get_rule(13); IF(OR(v=""; v="--"; v="NOT_FOUND"); IF(is_land; "Auffüllen"; "Standard"); TRIM(v)));
  output_format; LET(v; get_rule(15); IF(OR(v=""; v="--"; v="NOT_FOUND"); IF(is_land; "LAND"; "KREIS"); UPPER(TRIM(v))));
  
  tn_kreis; OR(foerder_umfang="TN_K"; foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF");
  tn_pauschal; OR(foerder_umfang="TN_P"; foerder_umfang="TN_P_MA_K"; foerder_umfang="TN_P_MA_P"; foerder_umfang="TN_P_MA_P_REF");
  tn_aktiv; OR(tn_kreis; tn_pauschal);
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; geo_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; geo_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; geo_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; "❌ Key: '" & rule_key & "' nicht gefunden";
    IF(INDEX(active_rows;1;1)="LEER"; "⚠️ Keine passenden Teilnehmer";
      IF(AND(min_tage > 0; event_tage < min_tage); "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht. Aktuell: " & event_tage;
        LET(
          col_geo; CHOOSECOLS(active_rows; geo_col_idx);
          col_fn; CHOOSECOLS(active_rows; 2);
          col_beh; CHOOSECOLS(active_rows; 4);
          col_soz; CHOOSECOLS(active_rows; 5);
          
          ages; CHOOSECOLS(active_rows; 26);
          age_ok; LAMBDA(a; fn; IF(OR(fn="MA"; fn="REF"); TRUE; IF(OR(a=""; NOT(ISNUMBER(a))); TRUE; AND(a >= min_alter_soft; a <= max_alter))));
          age_check; MAP(ages; col_fn; age_ok);
          filtered_age; IFERROR(FILTER(active_rows; age_check); "");
          
          fn_filtered; CHOOSECOLS(filtered_age; 2);
          all_tn; IFERROR(FILTER(filtered_age; fn_filtered="TN"); "");
          all_ma; IFERROR(FILTER(filtered_age; fn_filtered="MA"); "");
          all_ref; IFERROR(FILTER(filtered_age; fn_filtered="REF"); "");
          
          has_tn; AND(INDEX(all_tn;1;1)<>""; IFERROR(ROWS(all_tn)>0; FALSE));
          has_ma; AND(INDEX(all_ma;1;1)<>""; IFERROR(ROWS(all_ma)>0; FALSE));
          has_ref; AND(INDEX(all_ref;1;1)<>""; IFERROR(ROWS(all_ref)>0; FALSE));
          
          all_tn_cnt; IF(has_tn; ROWS(all_tn); 0);
          all_ma_cnt; IF(has_ma; ROWS(all_ma); 0);
          all_ref_cnt; IF(has_ref; ROWS(all_ref); 0);
          
          tn_geo; IF(all_tn_cnt=0; ""; CHOOSECOLS(all_tn; geo_col_idx));
          tn_locals_cnt; IF(all_tn_cnt=0; 0; COUNTIF(tn_geo; clean_geo));
          tn_locals; IF(tn_locals_cnt>0; FILTER(all_tn; tn_geo=clean_geo); "");
          
          local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
          tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
          
          quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
          use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
          
          final_tn; IF(NOT(tn_aktiv); ""; IF(all_tn_cnt=0; ""; IF(use_all; all_tn; IF(tn_locals_cnt>0; tn_locals; ""))));
          
          ma_geo; IF(all_ma_cnt=0; ""; CHOOSECOLS(all_ma; geo_col_idx));
          ma_locals_cnt; IF(all_ma_cnt=0; 0; COUNTIF(ma_geo; clean_geo));
          ma_locals; IF(ma_locals_cnt>0; FILTER(all_ma; ma_geo=clean_geo); "");
          
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
              col_geo_final; CHOOSECOLS(final_list; geo_col_idx);
              lokale; IFERROR(FILTER(final_list; col_geo_final=clean_geo); "");
              auswaertige; IFERROR(FILTER(final_list; col_geo_final<>clean_geo); "");
              lokale_sorted; IF(INDEX(lokale;1;1)=""; lokale; SORT(lokale; 12; TRUE));
              auswaertige_sorted; IF(INDEX(auswaertige;1;1)=""; auswaertige; SORT(auswaertige; 12; TRUE));
              has_lok; AND(INDEX(lokale_sorted;1;1)<>""; IFERROR(ROWS(lokale_sorted)>0; FALSE));
              has_aus; AND(INDEX(auswaertige_sorted;1;1)<>""; IFERROR(ROWS(auswaertige_sorted)>0; FALSE));
              IF(has_lok; IF(has_aus; VSTACK(lokale_sorted; auswaertige_sorted); lokale_sorted); IF(has_aus; auswaertige_sorted; "LEER"))
            )
          );
          
          cnt_final; IF(INDEX(final_list_sorted;1;1)="LEER"; 0; ROWS(final_list_sorted));
          
          IF(cnt_final = 0; "⚠️ Keine Personen nach Filter";
            IF(cnt_final < min_tn; "⚠️ Min TN (" & min_tn & ") nicht erreicht. Aktuell: " & cnt_final;
              IF(output_format = "KREIS";
                HSTACK(
                  MAP(CHOOSECOLS(final_list_sorted; 13); CHOOSECOLS(final_list_sorted; 12); LAMBDA(v;n; v&" "&n));
                  CHOOSECOLS(final_list_sorted; 16);
                  CHOOSECOLS(final_list_sorted; geo_col_idx);
                  MAP(CHOOSECOLS(final_list_sorted; 14); LAMBDA(d; TEXT(d; "dd.MM.yyyy")))
                );
                LET(
                  fn_col; CHOOSECOLS(final_list_sorted; 2);
                  beh_col; CHOOSECOLS(final_list_sorted; 4);
                  soz_col; CHOOSECOLS(final_list_sorted; 5);
                  bl_col; CHOOSECOLS(final_list_sorted; 28);
                  
                  col_f; MAP(fn_col; beh_col; LAMBDA(fn; beh; IF(fn="TN"; "Teilnehmer:in"; IF(fn="MA"; IF(OR(beh="BEGLEITPERSON"; beh="MmB_BEGLEITPERSON"); "Betreuer:in für Teilnehmende mit Behinderung"; "Betreuer:in für Teilnehmende ohne Behinderung"); IF(fn="REF"; "Referent:in"; fn)))));
                  
                  col_g; MAP(fn_col; beh_col; soz_col; LAMBDA(fn; beh; soz; LET(has_mmb; OR(beh="MmB"; beh="MmB_BEGLEITPERSON"); has_arb; soz="Arbeitslos"; has_eink; soz="Einkommensschwach"; role_txt; IF(fn="TN"; "Teilnehmer:in"; IF(fn="MA"; "Betreuer:in"; IF(fn="REF"; "Referent:in"; fn))); mmb_txt; IF(has_mmb; role_txt & " mit Behinderung"; ""); arb_txt; IF(has_arb; "Arbeitslose:r " & role_txt; ""); eink_txt; IF(has_eink; "einkommensschwach"; ""); TEXTJOIN(" und" & CHAR(10); TRUE; mmb_txt; arb_txt; eink_txt))));
                  
                  col_c; MAP(bl_col; LAMBDA(bl; IF(bl<>""; "Deutschland"; "Ausland")));
                  
                  HSTACK(
                    CHOOSECOLS(final_list_sorted; 12);
                    CHOOSECOLS(final_list_sorted; 13);
                    col_c;
                    CHOOSECOLS(final_list_sorted; 16);
                    CHOOSECOLS(final_list_sorted; 17);
                    col_f;
                    col_g;
                    CHOOSECOLS(final_list_sorted; 6);
                    MAP(CHOOSECOLS(final_list_sorted; 14); LAMBDA(d; TEXT(d; "yyyy")))
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

## Verwendung

### Für Kreis-Listen (z.B. Rhein-Lahn-Kreis)

CACHE_RULES Einstellungen:
- `GEO_LEVEL` = `LANDKREIS`
- `OUTPUT_FORMAT` = `KREIS`
- `FOERDER_UMFANG` = z.B. `TN_K_MA_K`

### Für Land-Listen (z.B. Rheinland-Pfalz)

CACHE_RULES Einstellungen:
- `GEO_LEVEL` = `BUNDESLAND`
- `OUTPUT_FORMAT` = `LAND`
- `FOERDER_UMFANG` = z.B. `TN_P_MA_P_REF`

---

## Änderungshistorie

**V6.1 (2026-01-20):**
- Kommentare entfernt (Google Sheets unterstützt keine // Kommentare)
- Zirkuläre Abhängigkeit bei geo_level_raw behoben

**V6 (2026-01-20):**
- Initiale Master-Formel basierend auf rheinlahnkreisV6 und rheinlandpfalzV6
- Dynamisches GEO_LEVEL (Landkreis/Bundesland)
- 12 Förderumfang-Codes mit REF
- Konfigurierbares OUTPUT_FORMAT (KREIS/LAND)
- Sortierung: Lokal zuerst, dann alphabetisch
