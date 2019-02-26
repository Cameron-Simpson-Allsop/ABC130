double TimetoEpoch(std::string time)
{
  
  double hours = std::stod(time.substr(0,2));
  double minutes = std::stod(time.substr(3,2));
  double seconds = std::stod(time.substr(6,2));
  
  double epoch = hours + (minutes/60) + (seconds/(60*60));//hours

  return epoch;
}
