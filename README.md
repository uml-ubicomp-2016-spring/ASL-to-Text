# ASL-to-Text
Simple ASL-to-Text translator using the LeapMotion

## Contributors
+ [TycheLaughs](http://github.com/TycheLaughs)
+ [KDibble](http://github.com/KDibble)
+ [jasminemoran](http://github.com/jasminemoran)

## Demo Video:
[![Demo Video](/utils/img/asl2txt.png)](https://drive.google.com/file/d/0B0DhBKfxZvDISU1EU3RKd2lxMWc/view?usp=drivesdk)

## Progress (Week 4/25 - 4/29 and 4/29 - 5/2)
- [x] Implement motion gestures
- [x] Break up potential words with spaces
- [x] Disallow an abundance of concurrent matches based on the large sets of frames used to match
- [x] Allow concurrent matches if user's hand is briefly absent as is necessary for various cases (e.g, 'ee', 'll', 'ff')
- [x] Project report (group)
- [x] Project report (individual)
- [x] Demo video
- [x] Project presentation materials

## Progress (Week 4/19 - 4/25)
- [ ] Implement motion gestures
- [x] Gather the rest of the data for required gestures

## Progress (Week 4/12 - 4/18)
- [x] Integrate machine learning into gestures
- [x] Gather all of the data for the required gestures (MOSTLY)

## Progress (Week 4/04 - 4/11)
- [ ] ~~Improve matching algorithms/expand pool of matches~~
- [x] Machine learning research: Using scikit-learn
- [x] Code refactor and cleanup

## Progress (Week 3/29 - 4/04)
- [x] All team members have forked the repo
- [x] Collect data for more letters than just 'A' and match them
- [x] Construct a method to find matches
- [ ] ~~Determine best way to store sign data~~ --reassessing
- [x] Formulate a way to make matches orientation-independent except for special cases

## Progress (Week 3/21 - 3/28)
- [x] Detect and print 'A'
- [x] A GUI prints text to the screen
- [x] GUI is rewritten in the MVC pattern, updates on new input
- [x] GUI has a single-function interface for use in accepting new text
- [x] Program recognizes built-in Leap gestures and reports them to GUI
