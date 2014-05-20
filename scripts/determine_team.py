

# Load the existing mapping from a txt
def load_mapping():
  mapping = {}

  f = open('abbreviation_to_team.txt', 'r')
  for line in f:
    [abbr, team] = line.split('\t')
    team = team.strip()
    if abbr not in mapping:
      mapping[abbr] = [team]
    else:
      mapping[abbr] = mapping[abbr] + [team]
  
  f.close()
  return mapping

# Decide which team it belongs to or ask user for input
def decide(home, away, abbr, other = None):
  mapping = load_mapping()
  if abbr in mapping:
    if home in mapping[abbr]:
      return True
    if away in mapping[abbr]:
      return False

    print 'Current mapping for this abbr is: ' + str(mapping[abbr])

  if other and other in mapping:
    if home in mapping[other]:
      f = open('abbreviation_to_team.txt', 'a')
      f.write(abbr + '\t' + away)
      f.write('\n')
      f.close()
      return False
    if away in mapping[other]:
      f = open('abbreviation_to_team.txt', 'a')
      f.write(abbr + '\t' + home)
      f.write('\n')
      f.close()
      return True

  print 'Home is ' + home
  print 'Away is ' + away
  response = raw_input("Which is this abbreviation for? 1 for HOME, 0 for AWAY: " + abbr + ' ? ')

  if response == '1':
    f = open('abbreviation_to_team.txt', 'a')
    f.write(abbr + '\t' + home)
    f.write('\n')
    f.close()
    return True
  if response == '0':
    f = open('abbreviation_to_team.txt', 'a')
    f.write(abbr + '\t' + away)
    f.write('\n')
    f.close()
    return False

  return decide(home, away, abbr)
    
if __name__ == "__main__":
  decide('Johnson &amp; Wales', '(RI) Norwich', 'NOR')
  decide('SUNY Cobleskill', 'Morrisville St.' , 'MORM')
  decide('SUNY Cobleskill', 'Morrisville St.' , 'COBM')
