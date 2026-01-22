=LET(
  m; M1:M1710;
  idx; SEQUENCE(1710; 1);
  maske; MAP(idx; m; LAMBDA(i; val; 
    WENN(i=1; "Zone 1: INPUT_ONLINE_AUSGABE";
    WENN(ODER(i=2; i=753; i=1458); "Lfd. Nr.";
    WENN(i=752; "Zone 2: INPUT_LOCAL_AUSGABE";
    WENN(i=1457; "Zone 3: INPUT: Manuelle Eingabe";
    WENN(ODER(i=750; i=751; i=1455; i=1456); "";
    WENN(val=""; ""; "ZÄHLEN"))))))
  ));
  zaehler; SCAN(0; maske; LAMBDA(acc; cur; WENN(cur="ZÄHLEN"; acc + 1; acc)));
  MAP(maske; zaehler; LAMBDA(m_val; z_val; WENN(m_val="ZÄHLEN"; z_val; m_val)))
)