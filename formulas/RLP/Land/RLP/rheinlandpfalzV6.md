# Formel für Land Rheinland-Pfalz V6

**Status:** ✅ v6 – Erweitert mit quote_modus, logik_modus, Sortierung und 12 Förderumfang-Codes  
**Basis:** V5 TN_LISTE-Struktur (29 Spalten)

## Änderungen V5 → V6

| Feature | V5 | V6 |
|---------|----|----|
| quote_modus | ❌ Hardcoded PROZENT | ✅ PROZENT/MEHRHEIT aus CACHE_RULES |
| logik_modus | ❌ Hardcoded | ✅ Standard/Auffüllen aus CACHE_RULES |
| foerder_umfang | ❌ Nicht verwendet | ✅ 12 Codes mit REF |
| Sortierung | ❌ Keine | ✅ Bundesland → Alphabetisch |
| Altersfilter | TN (MA/REF ausgenommen) | TN (MA/REF ausgenommen) ✅ |

---

## CACHE_RULES Keys

| Key | Event-Typ |
|-----|-----------|
| `Rheinland-Pfalz_Soziale_Bildung` | Soziale_Bildung |
| `Rheinland-Pfalz_Schulung_Ehrenamtlicher_Mitarbeitenden` | Schulung |
| `Rheinland-Pfalz_Politische_Jugendbildung` | Politische_Jugendbildung |

---

## Output-Spalten

| Spalte | Feld | Quelle/Logik |
|--------|------|--------------|
| A | Name | Index 12 |
| B | Vorname | Index 13 |
| C | Wohnort | `IF(Bundesland<>""; "Deutschland"; "Ausland")` |
| D | PLZ | Index 16 |
| E | Ort | Index 17 |
| F | Teilgenommen als | F-Logik |
| G | Eigenschaften | G-Logik |
| H | Anwesenheit | Index 6 |
| I | Geburtsjahr | `YEAR(Index 14)` |

---

## F-Logik (Teilgenommen als)

| Funktion | Behinderung | Ausgabe |
|----------|-------------|---------|
| TN | * | Teilnehmer:in |
| MA | `--` / `MmB` | Betreuer:in für Teilnehmende ohne Behinderung |
| MA | `BEGLEITPERSON` / `MmB_BEGLEITPERSON` | Betreuer:in für Teilnehmende mit Behinderung |
| REF | * | Referent:in |

## G-Logik (Eigenschaften)

Multi-Wert mit " und" + Zeilenumbruch (`CHAR(10)`).

| Bedingung | TN | MA | REF |
|-----------|----|----|-----|
| MmB / MmB_BEGLEITPERSON | Teilnehmer:in mit Behinderung | Betreuer:in mit Behinderung | Referent:in mit Behinderung |
| Arbeitslos | Arbeitslose:r Teilnehmer:in | Arbeitslose:r Betreuer:in | Arbeitslose:r Referent:in |
| Einkommensschwach | einkommensschwach | einkommensschwach | einkommensschwach |

---

## Förderumfang-Codes (12 Codes)

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
| `TN_P_MA_P_REF` | P | P | P | Alle (Standard für Land) |
| `REF` | — | — | P | Nur alle REF |

> **Standard für Land RLP:** `TN_P_MA_P_REF`

---

## Formel

```excel
=LET(
  debug_mode; SETUP!B69="Ja";
  ziel_bundesland; "Rheinland-Pfalz";
  event_typ_raw; SETUP!B18;
  event_start; SETUP!B23;
  event_ende; SETUP!H23;
  cache_rules; CACHE_RULES!A:Z;
  clean_event; SUBSTITUTE(TRIM(CLEAN(event_typ_raw)); " "; "_");
  rule_key; ziel_bundesland & "_" & clean_event;
  
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
  
  bl_z1; TN_LISTE!AC3:AC749;
  bl_z2; TN_LISTE!AC754:AC1454;
  bl_z3; TN_LISTE!AC1459:AC1710;
  
  get_rule; LAMBDA(col; IFERROR(VLOOKUP(rule_key; cache_rules; col; 0); "NOT_FOUND"));
  rule_check; get_rule(1);
  
  foerder_umfang; LET(v; get_rule(5); IF(OR(v=""; v="--"; v="NOT_FOUND"); "TN_P_MA_P_REF"; TRIM(v)));
  min_tn; LET(v; get_rule(6); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_alter; LET(v; get_rule(7); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  max_alter; LET(v; get_rule(8); IF(OR(v=""; v="--"; v="NOT_FOUND"); 999; VALUE(v)));
  min_alter_soft; LET(v; get_rule(9); IF(OR(v=""; v="--"; v="NOT_FOUND"); min_alter; VALUE(v)));
  min_tage; LET(v; get_rule(10); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote_raw; LET(v; get_rule(11); IF(OR(v=""; v="--"; v="NOT_FOUND"); 0; VALUE(v)));
  min_quote; IF(min_quote_raw > 1; min_quote_raw / 100; min_quote_raw);
  quote_modus; LET(v; get_rule(12); IF(OR(v=""; v="--"; v="NOT_FOUND"); "PROZENT"; UPPER(TRIM(v))));
  logik_modus; LET(v; get_rule(13); IF(OR(v=""; v="--"; v="NOT_FOUND"); "Auffüllen"; TRIM(v)));
  
  tn_kreis; OR(foerder_umfang="TN_K"; foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF");
  tn_pauschal; OR(foerder_umfang="TN_P"; foerder_umfang="TN_P_MA_K"; foerder_umfang="TN_P_MA_P"; foerder_umfang="TN_P_MA_P_REF");
  tn_aktiv; OR(tn_kreis; tn_pauschal);
  
  ma_kreis; OR(foerder_umfang="TN_K_MA_K"; foerder_umfang="TN_P_MA_K"; foerder_umfang="MA_K"; foerder_umfang="TN_K_MA_K_REF");
  ma_pauschal; OR(foerder_umfang="TN_K_MA_P"; foerder_umfang="TN_P_MA_P"; foerder_umfang="MA_P"; foerder_umfang="TN_P_MA_P_REF");
  ma_aktiv; OR(ma_kreis; ma_pauschal);
  
  ref_aktiv; OR(foerder_umfang="TN_K_REF"; foerder_umfang="TN_K_MA_K_REF"; foerder_umfang="TN_P_MA_P_REF"; foerder_umfang="REF");
  
  filtered_z1; IFERROR(FILTER(raw_z1; status_z1="Angemeldet"; bl_z1<>""); "");
  filtered_z2; IFERROR(FILTER(raw_z2; status_z2="Angemeldet"; bl_z2<>""); "");
  filtered_z3; IFERROR(FILTER(raw_z3; status_z3="Angemeldet"; bl_z3<>""); "");
  
  has_z1; AND(ROWS(filtered_z1)>0; filtered_z1<>"");
  has_z2; AND(ROWS(filtered_z2)>0; filtered_z2<>"");
  has_z3; AND(ROWS(filtered_z3)>0; filtered_z3<>"");
  
  active_rows; IF(has_z1; IF(has_z2; IF(has_z3; VSTACK(filtered_z1; filtered_z2; filtered_z3); VSTACK(filtered_z1; filtered_z2)); IF(has_z3; VSTACK(filtered_z1; filtered_z3); filtered_z1)); IF(has_z2; IF(has_z3; VSTACK(filtered_z2; filtered_z3); filtered_z2); IF(has_z3; filtered_z3; "LEER")));
  
  IF(rule_check="NOT_FOUND"; IF(debug_mode; "❌ Key: '" & rule_key & "' nicht gefunden"; "");
    IF(INDEX(active_rows;1;1)="LEER"; IF(debug_mode; "⚠️ Keine passenden Teilnehmer"; "");
      IF(AND(min_tage > 0; event_tage < min_tage); IF(debug_mode; "⚠️ Mindestdauer (" & min_tage & " Tage) nicht erreicht. Aktuell: " & event_tage; "");
        LET(
          col_bl; CHOOSECOLS(active_rows; 28);
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
          
          tn_bl; IF(all_tn_cnt=0; ""; CHOOSECOLS(all_tn; 28));
          tn_locals_cnt; IF(all_tn_cnt=0; 0; COUNTIF(tn_bl; ziel_bundesland));
          tn_locals; IF(tn_locals_cnt>0; FILTER(all_tn; tn_bl=ziel_bundesland); "");
          
          local_percent; IF(all_tn_cnt > 0; tn_locals_cnt / all_tn_cnt; 0);
          tn_auswaertige_cnt; all_tn_cnt - tn_locals_cnt;
          
          quote_erfuellt; IF(min_quote = 0; TRUE; IF(quote_modus = "PROZENT"; local_percent >= min_quote; tn_locals_cnt > tn_auswaertige_cnt));
          use_all; AND(quote_erfuellt; logik_modus="Auffüllen");
          
          final_tn; IF(NOT(tn_aktiv); ""; IF(all_tn_cnt=0; ""; IF(use_all; all_tn; IF(tn_locals_cnt>0; tn_locals; ""))));
          
          ma_bl; IF(all_ma_cnt=0; ""; CHOOSECOLS(all_ma; 28));
          ma_locals_cnt; IF(all_ma_cnt=0; 0; COUNTIF(ma_bl; ziel_bundesland));
          ma_locals; IF(ma_locals_cnt>0; FILTER(all_ma; ma_bl=ziel_bundesland); "");
          
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
              col_bl_final; CHOOSECOLS(final_list; 28);
              rlp_rows; IFERROR(FILTER(final_list; col_bl_final=ziel_bundesland); "");
              other_rows; IFERROR(FILTER(final_list; col_bl_final<>ziel_bundesland); "");
              rlp_sorted; IF(INDEX(rlp_rows;1;1)=""; rlp_rows; SORT(rlp_rows; 12; TRUE));
              other_sorted; IF(INDEX(other_rows;1;1)=""; other_rows; SORT(other_rows; 12; TRUE));
              has_rlp; AND(INDEX(rlp_sorted;1;1)<>""; IFERROR(ROWS(rlp_sorted)>0; FALSE));
              has_other; AND(INDEX(other_sorted;1;1)<>""; IFERROR(ROWS(other_sorted)>0; FALSE));
              IF(has_rlp; IF(has_other; VSTACK(rlp_sorted; other_sorted); rlp_sorted); IF(has_other; other_sorted; "LEER"))
            )
          );
          
          cnt_final; IF(INDEX(final_list_sorted;1;1)="LEER"; 0; ROWS(final_list_sorted));
          
          IF(cnt_final = 0; IF(debug_mode; "⚠️ Keine Personen nach Filter"; "");
            IF(cnt_final < min_tn; IF(debug_mode; "⚠️ Min TN (" & min_tn & ") nicht erreicht. Aktuell: " & cnt_final; "");
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
                  MAP(CHOOSECOLS(final_list_sorted; 14); LAMBDA(d; IF(ISNUMBER(d); YEAR(d); IFERROR(YEAR(DATEVALUE(d)); d))))
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

**V6.2 (2026-01-21):**
- DEBUG_MODUS hinzugefügt: `SETUP!B69` = "Ja"/"Nein"
- Alle Fehlermeldungen werden nur bei debug_mode=TRUE angezeigt

**V6.1 (2026-01-20):**
- Kommentare entfernt (Google Sheets unterstützt keine // Kommentare)

**V6 (2026-01-20):**
- `quote_modus` aus CACHE_RULES (PROZENT/MEHRHEIT)
- `logik_modus` aus CACHE_RULES (Standard/Auffüllen)
- `foerder_umfang` mit 12 Codes (inkl. REF)
- Sortierung: Bundesland (RLP zuerst) → Alphabetisch
- TN/MA/REF separate Filter und VSTACK
- Rückwärtskompatibel mit V5

**V5.1 (2026-01-19):**
- Altersfilter: MA/REF ausgenommen
- F-Logik: REF → "Referent:in"
- G-Logik: Kontextabhängig (Teilnehmer:in/Betreuer:in/Referent:in)
- Trenner: "und" statt "oder"

**V5.0 (Initial):**
- Basierend auf V5 TN_LISTE-Struktur (29 Spalten)
- Filter: Bundesland statt Landkreis
- Output: 9 Spalten
- Behinderung-Werte: MmB, BEGLEITPERSON, MmB_BEGLEITPERSON
