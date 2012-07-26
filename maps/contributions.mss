#contributions[zoom>=8] {
  ::outline {
    line-color: #808;
    line-width: 1;
    line-opacity: 0.4;
    line-join: round;
  }
  
  polygon-opacity: .0;
  
  [total_count >= 5] {
    [percent_obama >= 0.0]{ polygon-fill: #f00; polygon-opacity: .8; }
    [percent_obama > 0.2]{ polygon-fill: #c04; polygon-opacity: .6; }
    [percent_obama > 0.4]{ polygon-fill: #808; polygon-opacity: .4; }
    [percent_obama > 0.6]{ polygon-fill: #40c; polygon-opacity: .6; }
    [percent_obama > 0.8]{ polygon-fill: #00f; polygon-opacity: .8; }
  }
}
