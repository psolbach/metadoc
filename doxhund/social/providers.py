"""While we're only interested in share, like, up counts for now,
there's a lot of interesting metadata in e.g. reddit responses like
user_reports, report_reasons, num_reports, that might be useful
in building certain heuristics.
"""

providers = [
  {
    "provider": "facebook",
    "endpoint": "https://graph.facebook.com/?id={0}",
    "metrics": [{
      "label": "sharecount",
      "path": "share.share_count"
    }]
  },
  {
    "provider": "linkedin",
    "endpoint": "https://www.linkedin.com/countserv/count/share?url={0}/&format=json",
    "metrics": [{
      "label": "sharecount",
      "path": "count"
    }]
  },
  {
    "provider": "reddit",
    "endpoint": "https://buttons.reddit.com/button_info.json?url={0}",
    "metrics": [{
      "label": "upvotes",
      "path": "data.children[0].data.ups"
    },
    {
      "label": "num_reports",
      "path": "data.children[0].data.num_reports"
    }]
  }
]