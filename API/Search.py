def get_query(anime_name=None, filter=None, limit=5, page=1):
    """
    This function modified an sql query based on the filter selected.

    Args:
        anime_name (str, default=None): Name of anime.
        filter (str, default=None): How to order the return result.
        limit (int, default=5): limit the amount of items returned.
        page (int, default=1): what page number to scroll to.

    Returns:
        A string respresntation of an SQL query.
    """

    if not isinstance(limit, int):
        limit = 5
    if not isinstance(page, int):
        page = 1
    if anime_name is None or not isinstance(anime_name, str):
        query = "SELECT Anime_id, Name, Image FROM Anime"
    else:
        query = f"SELECT Anime_id, Name, Image FROM Anime WHERE Name LIKE '%{anime_name}%'"

    if filter:
        if filter.lower() == 'asc':
            query += " ORDER BY Name ASC"
        elif filter.lower() == 'desc':
            query += " ORDER BY Name DESC"
        elif filter.lower() == 'year':
            query += " ORDER BY Year ASC"
        elif filter.lower() == 'genre':
            query += " ORDER BY Genre ASC"

    query += f" LIMIT {limit}"
    if page > 1:
        query += f" OFFSET {limit * (page - 1)}"
    return query
