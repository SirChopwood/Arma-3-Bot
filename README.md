# Ramiris' Arma 3 Discord Bot
**Logistics Officer Mason#1954**
*& Logistics Servo-Skull-425#2971*

## Info

* Written in ``Python 3.8``
* The bot primarily the ``DiscordPy`` & ``MongoDB`` Libraries.
* All code is written and maintained by Ramiris#5376
* Data is stored on a custom MongoDB server, alongside the bot itself.

## Setup

1. [Invite the bot](https://discord.com/oauth2/authorize?client_id=743439007777685537&scope=bot&permissions=0)

2. Ensure the bot has relevant permissions. These can be set on the bot specific role or a generic one.
   * Needs permissions to edit the roles and manage nicknames of any roles/users you want managed.
   * Permission to read, send and manage messages in channels you want it active in.

3. Setup a default landing channel. This channel is one that any new user can see into when they join. Its recommended they can **only** see this channel and relevant one such as rules. Then set a new Role to be your member role. This role allows access into the main majority of your channels and categories.

4. Now use the ``INSERT COMMAND FOR SETTING REGISTER ROLE`` command to set the member role on the bot. This will mean that the bot will give new users this role once they have registered with the bot in **your** server. *Note: Your user data (meaning registration) is PER server. and will not carry over between them.*

5. Next you will want to modify the Ranks available to you in your server. You can do this via the following commands. Ranks are simply a form of title and visual state for the user, they do NOT affect what powers people have. *Ref: Rank Commands and Rank Formatting*

6. Now you have ranks, you will want to setup your Sections (Squads, Platoons, Groups, Detachments etc...). The sections you create should mirror the structure of your unit. A single Section is limited to 24 people due to Discord Embed limits. Some users in the section can be given admin access to that section. However no hierarchy of Sections exists, each one must internally administrate and/or be controlled by normal server admins. *Ref: Section Commands*

7. You are now in a position where the full extent of the bot is available! Feel free to use the ``>help`` command or look down at the different documentations below. *I personally recommend checking out Announcements, Suggestion Channels & Leave of Absence Channels.*


## Rank Commands

| Command | Description |
|:---:|:---:|
|``>ranks`` | Displays all the Ranks on the server along with their ID.
|``>rank_add (Rank Name)`` | Adds a new Rank with the specified name.
|``>rank_role (Rank ID)`` | Sets the role that the User will be added to when they receive the specified Rank.
|``>rank_long (Rank ID)`` | Sets the long name of the specified Rank.
|``>rank_short (Rank ID)`` | Sets the short name of the specified Rank.
|``>rank_format (Rank ID)`` | Sets the formatting of the specified Rank. (See Rank Formatting)
|``>rank_set (@User)`` | Sets the mentioned User to the rank number specified.
|``>rank_remove (Rank ID)`` | Removes the specified Rank. *NOTE: Rank 0 cannot be removed as it is the default*
|``>sername (@User)`` | Re-Sets the formatted name for the user. 


## Rank Formatting

Rank Formatting allows you to set how a user's name will be automatically formatted from their Rank and Profile.

To set the format of a rank, use ``>rank_format (ID)`` 

| Placeholder | Variable |
|:---:|:---:|
|``$RL``| Rank Long
|``$RS``| Rank Short
|``$FN``| First Name
|``$LN``| Last Name
|``$FI``| First Initial
|``$LI``| Last Initial
|``$NN``| Nickname

*NOTE: Nickname has to be manually set by the user via ``>profile_nickname (nickname)``. All other stats should exist by default.*

#### Example
| Variable | Meaning |
|:---:|:---|
|First Name|"Aether"
|Last Name|"Ramiris"
|Nickname|"Aether-425"
|Rank Long|"Adeptus Mechanicus Tech-Priest"
|Rank Short|"Enginseer"

* Format:``$RS $NN``
* Result: *Enginseer Aether-425*

* Format:``$RS. $FI. $LN``
* Result: *Enginseer. A.Ramiris*

## Section Commands

| Command | Description |
|:---:|:---:|
|``>section (Section Name)`` | Displays a section, including all members and their sign up status for all upcoming operations.
|``>section_add (Section Name)`` | Creates a new Section.
|``>section_colour (Hex code without the #)`` | Sets the colour of the Section.
|``>section_name (Old Name)\|(New Name)`` | Renames a Section.
|``>section_slot_add (Section Name)`` | Adds a new Slot to the Section.
|``>section_slot_assign (Section Name)`` | Assigns a unit to a Slot.
