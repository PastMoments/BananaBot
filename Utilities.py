import discord

def retrieve_embed_field_index(field_name: str, embed: discord.Embed):
    """
    Retrieves the index of a embed field, or -1 if it doesn't exist.
    :param field_name: str
    :param embed: discord.Embed
    :return: int
    """
    for i, field in enumerate(embed.fields):
        if field.name == field_name:
            return i
    return -1
