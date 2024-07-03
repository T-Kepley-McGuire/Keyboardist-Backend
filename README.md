# Keyboardist Backend

**A typing instruction game**

## 1000 ft. Overview

This backend serves the frontend with sections of text to type and analytics concerning users' typing. The analytics are integrated into the server to provide corrective and guiding feedback so the user can intentionally work on weak points to better improve their typing abilities.

The backend inforces the following process on the client:
1. Client requests text
2. Client types text
3. Metrics are recorded and sent back while typing
4. Typing is analyzed and analytics are added to client profile
5. Analytics are sent to the client
6. New texts are suggested based on client analytics.

The backend uses a specific algorithm to determine what the client should focus their energy on to improve their typing quickly.

### The algorithm

Characters that occur more frequently have the greatest impact on typing speed. If a typist has the option of working on 'e' or 'v' and improving their speed in typing each character by 5ms per keystroke, it is obvious that 'e' would be the appropriate choice to focus on. However if they could improve each character by 5%, this might change things as 'v' might be such a slow character to type that improving it by 5% might outweigh the relative lack of frequency of appearance in comparison to 'e'. If a character is half as frequent as another character, it becomes advantageous to work on that character if it is twice as slow or slower to type than the other character. If it is a third as frequent, it must be three times as slow to type. 

This basis is a good start but makes the core assumption that a typist can improve any character by an equal percentage. This is simply not the case. Some characters are easier to improve than others. Which characters requires a little more depth. 

If a character is typed more frequently, it is assumed to be closer to it's peak typing speed and thus more difficult to improve.

If a character has many neighbors (keys which share the finger that types that character), it is assumed that it would be more difficult to improve because the finger has many "hats" it must wear in a regular typing session. For instance, the character 'a' has far fewer neighbors than the character 'r' on a standard qwerty keyboard. Focusing on 'a' might be more advantageous since that finger can develop a more consistent muscle memory.

An equation can be developed from this:
```
coefficient of improvement = 
		frequency(char)^2 *
		sum(frequency(neighbors(char))) *
		speed(char)
```

Each character is scored using this coefficient of improvement. High coefficients communicate a likely greater increase in overall speed if the typist focuses on that character.

After scoring each character that a user types in a session (or rather the average thereof), users are suggested texts to type based on their weakest characters (highest coefficients of improvement). Currently this is done by having a bank of texts which are scored by the relative frequency of appearance of each character and selecting the texts which have the highest relative frequency in characters that have a high coefficient of improvement. 

A future potential feature would be to generate suggested texts from GPT or some other LLM while prompting it to focus on certain characters. Initial tests show that ChatGPT has the ability to generate paragraphs of text that utilize certain characters more than others while maintaining logical continuity (a feature which the author believes is essential for realistic typing practice). This would be quite cheap. A user could generate hundreds of paragraphs while only incurring minmal charges according to OpenAI pricing models. Further savings could be made by storing the generated texts in the database for future use, although it must be analyzed whether storage costs would outweigh generation costs (very unlikely but one has to make sure). A highbrid aproach could also be taken by storing texts which focus on more common weak characters. Some body of user analytics would have to be analyzed before a strong consensus on which characters are common could be established. However, as users generate texts, the distribution of weak characters would naturally arise in the texts generated, giving a large amount of options for common weak characters and fewer for less frequent weak characters. After a sufficient amount of texts are generated, server-side saving would be unnecessary as there would be enough variety to avoid repeating texts frequently. 

## Technical details

### API

*Coming soon...*

### Technology Stack

This server is built in Python using the Flask framework for routing and serving. Flask-SQLAlchemy is used to communicate with the PostgresSQL database which is hosted on AWS. Numpy is used for analysis.

### Database Schema

The database has the following tables:
* ```client```: the clients using the website
* ```typing_session```: one typing session/lesson including text reference, completion time, completion status (not implimented yet), and client reference
* ```text_section```: the body of text and a reference to the language it is in
* ```languages```: the potential languages a text may be in
* ```key_zones```: a reference to the text this zone gives info about, the name of the zone itself, and the prominence of this zone within the text (as a float)

Text sections are added to the database (text_section) labeled with their language (languages) and the properties of the text are analyzed (key_zones). 

Clients connect to the backend. If it is the first time, the a new client is created (client). Currently clients are identified by IP address. Then the client requests a new typing session to be opened (typing_session). They are provided with a typing session id and a section of text to type (text_section). 

While typing the section of text, updates are sent to the backend to store in the database (typing_session). Updates on a section of text must contain a session id which corresponds to a section of text that is open (status after creating before "closing" with either a complete or non-complete status). 

After the client is done typing, a close typing session request is sent and statistics are analyzed. Currently there is only global statistics but mayhaps they will be saved in their most recent tpying session data

## Credits

*Coming soon... (this app is not released yet; credits will be added before release)*