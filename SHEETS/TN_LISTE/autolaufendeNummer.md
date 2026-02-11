=LET(
  full_col; C2:C;
  is_angemeldet; MAP(full_col; LAMBDA(val; val="Angemeldet"));
  counts; SCAN(0; is_angemeldet; LAMBDA(acc; curr; WENN(curr; acc+1; acc)));
  result; MAP(is_angemeldet; counts; LAMBDA(hit; cnt; WENN(hit; cnt; "")));
  VSTACK("Nr."; result)
)