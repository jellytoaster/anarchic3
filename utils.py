import disnake
import classes.game
import classes.player
import classes.enums
emojis = {"mafia" : "<:mafia:1007768566789050378>", "evil": ":axe:", "good" : ":angel:", "randomtown" : "<:town:1007768656341651547>", "suspicious" : ":question:", "innocent" : ":thumbsup:", "neutral" : ":neutral_face:", "towninvestigative":"\🔎", "tm":"\🎶", "rt":"<:town:1007768656341651547>","townkilling":"\🔫","townprotective":"\💉","randommafia":"<:mafia:1007768566789050378>","ms":"\🥀","md":"\🎭","mk":"<:maf:891739940055052328>","ts":"\💬","associate": "<:assoicon:1006333104920735787>", "villager": "<:villyicon:1007714759409414274>", "associate": "<:assoicon:1006333104920735787>", "cop": "<:copicon2:889672912905322516>", "detective": "<:deticon2:889673135438319637>", "tracker": "<:trackicon:922885543812005949>", "lookout": "<:loicon2:889673190392078356>", "doctor": "<:docicon2:890333203959787580>", "vigilante": "<:enficon2:890339050865696798>", "attendant": "<:atticon:957688274418286602>", "psychic": "<:psyicon:1010900225130504192>", "mayor": "<:mayoricon:922566007946629131>", "mafioso": "<:maficon2:891739940055052328>", "framer": "<:frameicon2:890365634913902602>", "consigliere": "<:consigicon2:896154845130666084>", "janitor": "<:janiicon:923219547325091840>", "consort": "<:consicon2:890336628269281350>",  "headhunter": "<:hhicon2:891429754643808276>", "executioner": "<:hhicon2:891429754643808276>", "jester": "<:atticon:957688274418286602>", "framer": "<:framed:890365634913902602>", "agent": "<:agenticon2:1011769559662985246>", "lookout": "<:loicon2:1011291078248366110>,", "janitor": "<:janiicon:939311465796599818>", "bodyguard": "<:bgicon:1018521495439429702>"}

def roleEmoji(name:str):
    try:
        return emojis[name.lower()]
    except Exception as e:
        return ""

def isContraction(name:str):
    for val in classes.enums.Contractions:
        if name.lower() == val.value.lower():
            return True
    else:
        return False

async def createRoleIfNotExist(guild, roleName:str):
    if (disnake.utils.get(guild.roles, name=roleName) == None):
        return await guild.create_role(name=roleName, hoist=False, mentionable=True)
    else:
        return disnake.utils.get(guild.roles, name=roleName)
    
async def makePrivate(channel:disnake.channel.TextChannel):
    await channel.set_permissions(channel.guild.default_role, view_channel=False, read_messages=False)

async def modifySendPermissions(channel:disnake.channel.TextChannel, game:classes.game.Game, **kwargs):

    """
    Modifies the permissions of a channel.
    Parameters:
        channel: The channel to modify permissions for

    dead --> dead players

    alive --> alive playrers

    """


    #get roles to modify permissions for
    playerRole = game.rolePlayer
    deadRole = game.roleDead

    overwrite = channel.overwrites_for(deadRole)
    overwrite.send_messages = kwargs["dead"]
    await channel.set_permissions(deadRole, overwrite=overwrite)
    overwrite = channel.overwrites_for(playerRole)
    overwrite.send_messages = kwargs["alive"]
    await channel.set_permissions(playerRole, overwrite=overwrite)

async def modifyReadPermissoins(channel:disnake.channel.TextChannel, game:classes.game.Game, **kwargs):

    """
    Modifies the permissions of a channel.
    Parameters:
        channel: The channel to modify permissions for

    dead --> dead playres

    alive --> alive players

    """

    

    #get roles to modify permissions for
    playerRole = game.rolePlayer
    deadRole = game.roleDead

    overwrite = channel.overwrites_for(deadRole)
    overwrite.read_messages = kwargs["dead"]
    await channel.set_permissions(deadRole, overwrite=overwrite)
    overwrite = channel.overwrites_for(playerRole)
    overwrite.read_messages = kwargs["alive"]
    await channel.set_permissions(playerRole, overwrite=overwrite)

# Targeting options templates
def notMeAndNotDead(me, allPlayers):
    res = []
    for i in allPlayers:
        if (i.dead == False and i.memberObj.id != me.memberObj.id):
            res.append(i)

    return res

def notMafiaAndNotDead(me, allPlayers):
    res = []
    for i in allPlayers:
        if (i.dead == False and i.assignedRole.faction != classes.enums.Faction.Mafia):
            res.append(i)

    return res


def literallyAnyone(me, allPlayers):
    return allPlayers


def notDead(me, allPlayers):
    res = []
    for i in allPlayers:
        if (i.dead == False):
            res.append(i)

    return res


def reasonToText(reason:classes.enums.DeathReason, mention):
    if (reason == classes.enums.DeathReason.Unknown):
        return f"{mention} **disappeared**."
    # if (reason == DeathReason.GoingInsane):
    #     return "They gave up on Anarchic and left the Town."
    # if (reason == DeathReason.Unknown):
    #     return "They were killed of unknown causes."
    # if (reason == DeathReason.Suicide):
    #     return "They commited suicide."
    if (reason == classes.enums.DeathReason.Mafia):
        return f"{mention} was **attacked by the Mafia** <:mafia:1007768566789050378>"
    if (reason == classes.enums.DeathReason.Enforcer):
        return f"{mention} was **shot by a Vigilante** <:vgicon:890339050865696798>"
    # # if (reason == DeathReason.Guilt):
    # #     return "They died from **Guilt**."
    # if (reason == DeathReason.Jester):
    #     return "**killed over lynching the Jester** <:jesticon2:889968373612560394>."
    if (reason == classes.enums.DeathReason.Plague):
        return f"{mention} was **taken by the Plague**."
    # if (reason == DeathReason.Bodyguard):
    #     return "**killed by a Bodyguard**. <:bgicon:1018521495439429702>"
    # if (reason == DeathReason.WhileGuarding):
    #     return "**died while guarding someone.** <:bgicon:1018521495439429702>"
    # if (reason == DeathReason.Psychopath):
    #     return "They were killed by a member of the **Psychopath**."
    # if (reason == DeathReason.Cleaned):
    #     return "We could not determine how they died."

async def getCurrentLynch(votingData, game):
    """Utilises the class's voting data to generate a current lynch as a string. Will most likely throw an error when a invalid voting data is part of the class"""

    highestVote = 0
    highestVotePlayer = None
    isTied = False

    for key, value in votingData.items():
        if (type(value) is list):
            if (len(value) != 0):
                if (len(value) > highestVote):
                    highestVote = len(value)
                    player = classes.player.Player.get(key, game)
                    highestVotePlayer = player.memberObj.global_name
                    isTied == False
                elif (len(value) == highestVote):
                    isTied = True
    
    if (isTied == True):
        return "Tied"
    if (highestVote == 0):
        return "None"
    
    return highestVotePlayer

def createVotingResults(embed, game:classes.game.Game, guilties, innocents):
    
    embed.add_field(name="**`Guilty ✅`**", value="\n".join([i.memberObj.mention for i in guilties if i.dead == False]))

    embed.add_field(name="**`Pardon ❌`**", value="\n".join([i.memberObj.mention for i in innocents if i.dead == False]))

    abstained = list(set(game.playervar) - set(guilties) - set(innocents))

    embed.add_field(name="**`Abstain ☑️`**", value="\n".join([i.memberObj.mention for i in abstained if i.dead == False]))

    embed.set_footer(text="Most trial results are democratic")

    return embed

def chargeCount(charges):
    if (charges == -1):
        return "You will have unlimited charges left"
    elif (charges - 1 == 0):
        return "You will have no more charges left"
    else:
        return f"You will have {charges - 1} charges left"
    
def true(game):
    return True

def errorToText(errorStr:str):
    errorStr = errorStr.lower()
    if ("403" in errorStr):
        return "This can happen because either the bot does not have enough permissions to perform actions or the bot has been blocked by a user and a DM cannot be sent."
    else:
        return "This error is undocumented and has been automatically reported to the developers."

def errorToFix(errorStr:str):
    errorStr = errorStr.lower()
    if ("403" in errorStr):
        return "- Check the permissions the bot has\n- Make sure the bot has not been blocked by any user"
    else:
        return "- Wait until a fix has been applied"
    
async def finishGame(game:classes.game.Game):
    game.finished = True

    await modifySendPermissions(game.channelTownSquare, game, dead=True, alive=True)
    await modifyReadPermissoins(game.channelGraveyard, game, dead=True, alive=True)
    await modifySendPermissions(game.channelGraveyard, game, dead=True, alive=True)
    await modifyReadPermissoins(game.channelMafia, game, dead=True,alive=True)
    await modifySendPermissions(game.channelMafia, game, dead=True,alive=True)