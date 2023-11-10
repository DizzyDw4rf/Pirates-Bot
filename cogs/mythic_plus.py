import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Select, Button, View
from typing import List
from constants import *
from keystones import *


roles_ids_to_mention = [1149464248733409280]

class MythicPlus(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def payment_realms_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        realms = [
            "Area 52", "Bleeding Hollow", "Illidan", "Mal'Ganis", "Sargeras", "Stormrage", "Thrall", "Tichondrius"
        ]
        data = []
        for realm in realms:
            if current.lower() in realm.lower():
                data.append(app_commands.Choice(name=realm, value=realm))
        return data

    async def armor_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        armors = ["Plate", "Leather", "Mail", "Cloth"]
        data = []
        for armor in armors:
            if current.lower() in armor.lower():
                data.append(app_commands.Choice(name=armor, value=armor))
        return data

    @app_commands.command(name="mythic_plus", description="Mythic Plus looking for group")
    @app_commands.describe(
        level="Level of the dungeon.", 
        quantity="Number of runs.",
        server="Server to choose from.", 
        payment_realms="The realm you pay in.", 
        offerd_cuts="How many gold you affer per player.",
        dps="Number of Damage per second players.",
        healers="Number of Healers players.",
        tanks="Number of Tanks players.",
        armor="Choose the type of players you want.",
        timing="Timed or not.",
        buyer_info_participation="If buyer will participate in the dungeon.",
        note="Any notes you want players to know."
    )
    @app_commands.choices(
        server=[
        app_commands.Choice(name="US", value="US"),
        app_commands.Choice(name="EU", value="EU")
    ],dps=[
        app_commands.Choice(name="0", value=0),
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3)
    ],healers=[
        app_commands.Choice(name="0", value=0),
        app_commands.Choice(name="1", value=1)
    ],tanks=[
        app_commands.Choice(name="0", value=0),
        app_commands.Choice(name="1", value=1)
    ],timing=[
        app_commands.Choice(name="True", value="Timed ⏳"),
        app_commands.Choice(name="False", value="Not Timed 🚫")
    ],buyer_info_participation=[
        app_commands.Choice(name="True", value="Yes ✔"),
        app_commands.Choice(name="False", value="No 🚫")
    ])
    @app_commands.autocomplete(
        payment_realms=payment_realms_autocomplete,
        armor=armor_autocomplete)

    async def mythic_plus(
        self,
        interaction: discord.Interaction,
        level: int,
        quantity: int,
        server: app_commands.Choice[str],
        payment_realms: str,
        offerd_cuts: float,
        armor: str = None,
        dps: app_commands.Choice[int] = None,
        healers: app_commands.Choice[int] = None,
        tanks: app_commands.Choice[int] = None,
        timing: app_commands.Choice[str] = None,
        buyer_info_participation: app_commands.Choice[str] = None,
        note: str = "-"
    ):
        

        applied_users = []

        # Default parameters
        if dps is None:
            # default choice for dps
            dps = app_commands.Choice(name="2", value=2)
        if healers is None:
            # default choice for healers
            healers = app_commands.Choice(name="1", value=1)
        if tanks is None:
            # default choice for tanks
            tanks = app_commands.Choice(name="1", value=1)
        if timing is None:
            timing = app_commands.Choice(name="True", value="Timed ⏳")
        if buyer_info_participation is None:
            buyer_info_participation = app_commands.Choice(
                name="False", value="No 🚫")

        def get_eligible_armor_types(armor):
            if armor is None:
                return "Any", "Any", "Any"
            if armor == "Plate":
                return f"{DEATH_KNIGHT_ICON} Death Knight\n{WARRIOR_ICON} Warrior\n{PALADIN_ICON} Paladin", f"{PALADIN_ICON} Paladin", f"{DEATH_KNIGHT_ICON} Death Knight\n{WARRIOR_ICON} Warrior\n{PALADIN_ICON} Paladin"
            if armor == "Leather":
                return f"{DEMON_HUNTER_ICON} Demon Hunter\n{DRUID_ICON} Druid\n{MONK_ICON} Monk", f"{DRUID_ICON} Druid\n{MONK_ICON} Monk", f"{DEMON_HUNTER_ICON} Demon Hunter\n{DRUID_ICON} Druid\n{MONK_ICON} Monk\n{ROUGE_ICON} Rouge"
            if armor == "Mail":
                return "Any", f"{SHAMAN_ICON} Shaman\n{EVOKER_ICON} Evoker", f"{SHAMAN_ICON} Shaman\n{HUNTER_ICON} Hunter\n{EVOKER_ICON} Evoker"
            if armor == "Cloth":
                return "Any", f"{PRIEST_ICON} Priest", f"{MAGE_ICON} Mage\n{PRIEST_ICON} Priest\n{WARLOCK_ICON} Warlock"
            return "Any", "Any", "Any"  # Default Case

        eligible_tanks, eligible_healers, eligible_dps = get_eligible_armor_types(
            armor)

        mp = discord.Embed(
            title=f"MythicPlus +{level}x{quantity}", color=discord.Colour.brand_red())
        mp.add_field(
            name="Offered Cuts",
            value=f"{(offerd_cuts)}K 💰",
            inline=True
        )
        mp.add_field(
            name=f"Quantity: {quantity}\nLevel: {level}",
            value=f"{timing.value}",
            inline=True
        )
        mp.add_field(
            name="Server",
            value=f"{server.value}",
            inline=True
        )
        mp.add_field(
            name="Filling Progress",
            value=f"{TANK_Icon}\t0/{tanks.value}\n{HEALER_ICON}\t0/{healers.value}\n{DPS_ICON}\t0/{dps.value}",
            inline=True
        )
        mp.add_field(
            name="Payment Realms",
            value=f"{payment_realms}",
            inline=True
        )
        mp.add_field(
            name="Buyer Info\nParticibation",
            value=f"{buyer_info_participation.value}",
            inline=True
        )
        mp.add_field(
            name="keys",
            value=f"Any Key",
            inline=True
        )
        mp.add_field(
            name="Eligible Tank",
            value=f"{eligible_tanks}",
            inline=True
        )
        mp.add_field(
            name="Eligible Healer",
            value=f"{eligible_healers}",
            inline=True
        )
        mp.add_field(
            name="Eligible DPS",
            value=f"{eligible_dps}",
            inline=True
        )
        mp.add_field(
            name="Note",
            value=f"{note}"
        )
        mp.set_footer(text=f"{interaction.user.id}")

        mythic_keys = Select(
            custom_id="mythic_keys",
            min_values=1,
            max_values=4,
            placeholder="Choose spacific keys you want to play in.",
            options=[
                discord.SelectOption(
                    label="Any Key",
                    value=f"{DEFAULT_KEY} Any Key",
                    emoji=f"{DEFAULT_KEY}"
                ),
                discord.SelectOption(
                    label="Brackenhide Hollow",
                    value=f"{BRAKEN_HIDE_HOLLOW} Brackenhide Hollow",
                    emoji=f"{BRAKEN_HIDE_HOLLOW}"
                ),
                discord.SelectOption(
                    label="Freehold",
                    value=f"{FREE_HOLD} Freehold",
                    emoji=f"{FREE_HOLD}"
                ),
                discord.SelectOption(
                    label="Halls of Infusion",
                    value=f"{HALLS_OF_INFUSION} Halls of Infusion",
                    emoji=f"{HALLS_OF_INFUSION}"
                ),
                discord.SelectOption(
                    label="Neltharion's Lair",
                    value=f"{NELTHARIONS_LAIR} Neltharion's Lair",
                    emoji=f"{NELTHARIONS_LAIR}"
                ),
                discord.SelectOption(
                    label="Neltharus",
                    value=f"{NELTHARUS} Neltharus",
                    emoji=f"{NELTHARUS}"
                ),
                discord.SelectOption(
                    label="Uldaman: Legacy of Tyr",
                    value=f"{ULDAMAN_LEGACY_OF_TYR} Uldaman: Legacy of Tyr",
                    emoji=f"{ULDAMAN_LEGACY_OF_TYR}"
                ),
                discord.SelectOption(
                    label="The Underrot",
                    value=f"{THE_UNDERROT} The Underrot",
                    emoji=f"{THE_UNDERROT}"
                ),
                discord.SelectOption(
                    label="The Vortex Pinnacle",
                    value=f"{THE_VORTEX_PINNACLE} The Vortex Pinnacle",
                    emoji=f"{THE_VORTEX_PINNACLE}"
                )
            ]
        )

        async def mythic_keys_callback(interaction: discord.Interaction):
            selected_keys = interaction.data["values"]
            mp.set_field_at(6, name="keys", value='\n '.join(
                selected_keys), inline=True)
            await interaction.response.edit_message(embed=mp)

        async def finalize_button_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            roles_mentions = " ".join([f"<@&{role_id}>" for role_id in roles_ids_to_mention])
            buyer_selection_thread = await interaction.channel.create_thread(name=mp.title)

            async def booster_apply_button_callback(interaction: discord.Interaction):
                user = interaction.user
                if user not in applied_users:
                    await interaction.response.send_message(f"{interaction.user.mention} has applied")
                    applied_users.append(user)
                else:
                    await interaction.response.send_message(f"{interaction.user.mention} already applied")

            # Booster apply button view
            booster_apply_button = Button(
                style=discord.ButtonStyle.green, label="Apply", emoji="✔")
            booster_view = View()
            booster_apply_button.callback = booster_apply_button_callback
            booster_view.add_item(booster_apply_button)

            # Buyer select menu view
            selected_players_option = [
                discord.SelectOption(label="Select applicants", value="select_applicants", default=True)
            ]
            for user in applied_users:
                selected_players_option.append(
                    discord.SelectOption(label=user.display_name, value=str(user.id))
                )
            select_player = Select(
                custom_id="select_players",
                min_values=1,
                max_values=4,
                placeholder="Select applicants",
                options=selected_players_option
            )

            buyer_view = View()
            buyer_view.add_item(select_player)
            
            offers_channel_id = 1158856545916964864
            offers_channel = interaction.guild.get_channel(offers_channel_id)
            if offers_channel:
                await offers_channel.send(content=f"{roles_mentions}", embed=mp, view=booster_view)
            else:
                await interaction.response.send_message("Offers Channel cannot be found.")

            await buyer_selection_thread.send(embed=mp, view=buyer_view)

        finalize_button = Button(
            style=discord.ButtonStyle.green, label="Finalize", emoji="📧")
        finalize_button.callback = finalize_button_callback
        mythic_keys.callback = mythic_keys_callback
        mythic_keys_view = View()
        mythic_keys_view.add_item(mythic_keys)
        mythic_keys_view.add_item(finalize_button)
        await interaction.response.send_message(embed=mp, view=mythic_keys_view, ephemeral=True)


async def setup(client):
    await client.add_cog(MythicPlus(client))
