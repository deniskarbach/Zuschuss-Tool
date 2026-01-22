=WENNFEHLER(
BYROW(
  FILTER(INPUT_ONLINE!A2:AAN748; 
    REGEXMATCH(INPUT_ONLINE!A1:AAN1; "(?i)Stra.e|Haus_?nr|Nr\.|Anschrift|Adresse") * 
    NICHT(REGEXMATCH(INPUT_ONLINE!A1:AAN1; "(?i)E-?Mail"))
  ); 
  LAMBDA(zeile; TEXTJOIN(" "; WAHR; zeile))
);
"k.A.:Adresse"
)