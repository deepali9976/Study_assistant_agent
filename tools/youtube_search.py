from phi.tools import Toolkit
from youtubesearchpython import ChannelsSearch
from typing import Optional
from phi.utils.log import logger

class YouTubeChannelToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="youtube_channel_tools")
        self.register(self.search_channels)

    def search_channels(self, query: str, max_results: Optional[int] = 5) -> str:
        """Searches YouTube for channels matching the query."""
        logger.info(f"Searching YouTube channels for: {query}")
        try:
            channels_search = ChannelsSearch(query, limit=max_results)
            results = channels_search.result()
            links = []
            for channel in results.get("result", []):
                title = channel.get("title")
                link = channel.get("link")
                if title and link:
                    links.append(f"{title} - {link}")
            return "\n".join(links) if links else "No channels found."
        except Exception as e:
            logger.error(f"Channel search error: {e}")
            return f"Error: {e}"
