import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="NBA Team PPG Evolution",
    layout="wide",
)


# =============================================================================
# DATA LOADING  

@st.cache_data
def load_data():

    stats   = pd.read_csv(r"database/2021_26/teams_stats.csv")   
    teams   = pd.read_csv(r"database/2021_26/teams.csv")         
    seasons = pd.read_csv(r"database/2021_26/seasons.csv")       #


    yrs = seasons[["Season_ID"]]                        
    tms = teams[["Team_ID", "Team_Abbreviation",        
                 "Team_Name", "Team_Conference"]]
    

    # i.e. 5 seasons x 30 teams = 150 rows. This guarantees we have a row for
    # every team in every season even if the stats table has gaps.
    df = yrs.merge(tms, how='cross')


    df = df.merge(
        stats[["Season_ID", "Team_ID", "PTS", "G"]],
        on=["Season_ID", "Team_ID"]
    )
    df = df.merge(seasons[["Season_ID", "Season_Years"]], on="Season_ID")


    df["Team_PPG"] = df["PTS"]
    df = df.sort_values(["Season_Years", "Team_PPG"], ascending=[True, False])

    return df  

# Call load_data() once; result is cached for all subsequent reruns
team_ppg = load_data()


# =============================================================================
# Styling
# CUSTOM CSS  (injected as raw HTML)
# unsafe_allow_html=True is required whenever we pass real HTML to Streamlit.
# This block:
#   - Imports two Google Fonts (Bebas Neue for titles, DM Sans for body text)
#   - Forces the dark background on the whole page
#   - Styles the metric cards we build manually further down
# =============================================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
      background-color: #0d0d12;
      color: #e8e8e8;
      font-family: 'DM Sans', sans-serif;
  }
  h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }
  .block-container { padding: 2rem 3rem; }

  /* Orange highlight on multiselect tags in the sidebar */
  .stMultiSelect [data-baseweb="tag"] { background-color: #e8572a !important; }

  /* KPI card container */
  .metric-box {
      background: #16161e;
      border: 1px solid #2a2a38;
      border-radius: 10px;
      padding: 14px 20px;
      text-align: center;
  }
  .metric-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #888; }
  .metric-value { font-family: 'Bebas Neue'; font-size: 2rem; color: #e8572a; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SIDEBAR FILTERS
st.sidebar.markdown("## Filter")

#conference filtering
conferences = ["All"] + sorted(team_ppg["Team_Conference"].dropna().unique())
conf_sel = st.sidebar.selectbox("Conference", conferences)


all_teams = sorted(team_ppg["Team_Name"].unique())
team_sel  = st.sidebar.multiselect( 
    "Highlight teams",
    options=all_teams,
    default=[],
    placeholder="All teams shown — filter your wants"
)

#league average 
show_avg = st.sidebar.toggle("Show league average", value=True)



# APPLY FILTERS TO THE DATAFRAME
df = team_ppg.copy()

# If a specific conference was chosen, drop all rows from the other conference
if conf_sel != "All":
    df = df[df["Team_Conference"] == conf_sel]

# Sorted list of season labels — used for x-axis ordering and KPI lookups
seasons_ordered = sorted(df["Season_Years"].unique())

# Unique team names remaining after the conference filter is applied
teams_in_view = df["Team_Name"].unique()


# COLOUR PALETTE
PALETTE = [
    "#e8572a","#f0a500","#3ecfcf","#a78bfa","#34d399",
    "#f472b6","#60a5fa","#fbbf24","#4ade80","#fb7185",
    "#38bdf8","#c084fc","#f97316","#2dd4bf","#818cf8",
    "#fb923c","#a3e635","#e879f9","#22d3ee","#facc15",
    "#86efac","#fda4af","#93c5fd","#d8b4fe","#6ee7b7",
    "#fcd34d","#7dd3fc","#f0abfc","#a5f3fc","#fef08a",
]

team_colors = {t: PALETTE[i % len(PALETTE)] for i, t in enumerate(sorted(teams_in_view))}




# =============================================================================
# BUILD THE PLOTLY FIGURE

fig = go.Figure()

for team in teams_in_view:
    # Filter to this team's rows only, sorted chronologically so the line
    # is drawn left-to-right across the x-axis
    tdf  = df[df["Team_Name"] == team].sort_values("Season_Years")

    # Grab the 3-letter abbreviation from the first row (constant for every row)
    abbr = tdf["Team_Abbreviation"].iloc[0]

    # ── Highlight logic ───────────────────────────────────────────────────────
    # If the user selected specific teams: only those are "highlighted"
    # If no teams are selected:           all teams are treated as highlighted
    is_highlighted = (team in team_sel) if team_sel else True

    # Highlighted lines are thick and fully opaque; others fade to the background
    opacity  = 1.0 if is_highlighted else 0.12   # 0 = invisible, 1 = fully visible
    lw       = 2.8 if is_highlighted else 1.0    # line width in pixels
    marker_s = 8   if is_highlighted else 4      # data-point dot diameter in pixels

    # Add this team's line to the figure
    fig.add_trace(go.Scatter(
        x    = tdf["Season_Years"],   # x values: season label strings
        y    = tdf["Team_PPG"],       # y values: points per game floats
        mode = "lines+markers",       # draw both the connecting line and dots
        name = abbr,                  # text label shown in the legend
        line = dict(
            color     = team_colors[team],
            width     = lw,
            shape     = "spline",     # smooth curve (vs "linear" for straight segments)
            smoothing = 0.6           # 0 = straight lines, 1.3 = maximum curve
        ),
        marker = dict(
            size  = marker_s,
            color = team_colors[team],
            line  = dict(width=1.5, color="#0d0d12")  # dark ring around each dot for contrast
        ),
        opacity       = opacity,
        hovertemplate = (
            f"<b>{team}</b><br>"           # full team name, bolded
            "Season: %{x}<br>"             # %{x} is substituted with the x value on hover
            "PPG: <b>%{y:.1f}</b>"         # .1f formats to one decimal place
            "<extra></extra>"              # removes the secondary label Plotly adds by default
        ),
        legendgroup = team,   # ties the legend entry to this trace
    ))


# =============================================================================
# OPTIONAL LEAGUE AVERAGE OVERLAY
if show_avg:
    league_avg = (
        df.groupby("Season_Years", group_keys=False)
        .apply(lambda x: pd.Series({"Avg_PPG": x["PTS"].sum() / x["G"].sum()}))
        .reset_index()
    )

    fig.add_trace(go.Scatter(
        x    = league_avg["Season_Years"],
        y    = league_avg["Avg_PPG"].round(2),
        mode = "lines",                       # line only, no dots
        name = "League Avg",
        line = dict(color="#ffffff", width=2, dash="dot"),   # dotted white line
        opacity       = 0.55,
        hovertemplate = "League Avg<br>Season: %{x}<br>PPG: <b>%{y:.1f}</b><extra></extra>",
    ))


# =============================================================================
# FIGURE LAYOUT — global visual settings applied to the whole chart
fig.update_layout(
    paper_bgcolor = "#0d0d12",   # background colour outside the plot area
    plot_bgcolor  = "#0d0d12",   # background colour inside the plot area

    font = dict(family="DM Sans", color="#c8c8d0", size=13),   # default font for all text

    title = dict(
        text = "NBA Team Points Per Game — 2021 to 2026",
        font = dict(family="Bebas Neue", size=30, color="#ffffff"),
        x=0.01, y=0.97,   # 0.0 = far left, 1.0 = far right; 0.97 = near top
    ),

    xaxis = dict(
        title     = "Season",
        tickfont  = dict(size=12),
        gridcolor = "#1e1e2a",   # colour of the vertical grid lines
        linecolor = "#2a2a38",   # colour of the axis line itself
        showgrid  = True,
    ),

    yaxis = dict(
        title     = "Points Per Game (PPG)",
        tickfont  = dict(size=12),
        gridcolor = "#1e1e2a",
        linecolor = "#2a2a38",
        showgrid  = True,
        zeroline  = False, 
        range= [95, 125]
    ),

    # Legend sits to the right of the chart area
    legend = dict(
        orientation = "v",              # vertical stack of entries
        x=1.01, y=1,                    # just past the right edge of the plot
        bgcolor     = "rgba(13,13,18,0.85)",
        bordercolor = "#2a2a38",
        borderwidth = 1,
        font        = dict(size=11),
        title       = dict(
            text = "TEAM",
            font = dict(family="Bebas Neue", size=14, color="#e8572a")
        ),
    ),

    hovermode  = "closest",   # show tooltip for the single nearest point
    hoverlabel = dict(
        bgcolor     = "#16161e",
        bordercolor = "#2a2a38",
        font        = dict(family="DM Sans", size=13),
    ),

    # Padding around the plot area in pixels (left / right / top / bottom)
    margin = dict(l=60, r=160, t=80, b=60),
    height = 620,   # total figure height in pixels
)


# =============================================================================
# PAGE HEADER
st.markdown("# 2021=>26 TEAMS SCORING EVOLUTION")
st.markdown(
    "<p style='color:#888;font-size:14px;margin-top:-10px;'>"
    "Points Per Game by each franchise since 2021</p>",
    unsafe_allow_html=True,
)
st.markdown("---")   # renders a horizontal rule / divider


# =============================================================================
# SUMMARY numbers for the latest season
 
latest_season = seasons_ordered[-1]                             
latest_df     = df[df["Season_Years"] == latest_season]         

top_team    = latest_df.loc[latest_df["Team_PPG"].idxmax()]   
bottom_team = latest_df.loc[latest_df["Team_PPG"].idxmin()]     
league_ppg  = (latest_df["PTS"].sum() / 30).round(1) 

#layout
c1, c2, c3, c4 = st.columns(4)
for col, label, val in [
    (c1, f"🏆 Top scorer ({latest_season})",    f"{top_team['Team_Abbreviation']} — {top_team['Team_PPG']}"),
    (c2, f"📉 Lowest scorer ({latest_season})", f"{bottom_team['Team_Abbreviation']} — {bottom_team['Team_PPG']}"),
    (c3, "📊 League avg PPG",                   str(league_ppg)),
    (c4, "🏀 Teams tracked",                    str(len(teams_in_view))),
]:
    col.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{val}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True) 


# =============================================================================
# RENDER THE CHART
st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# COLLAPSIBLE RAW DATA TABLE
with st.expander("📋 View raw team PPG data"):

    # Select only display-relevant columns and rename them to friendly titles
    display_df = (
        df[["Season_Years", "Team_Name", "Team_Abbreviation", "Team_Conference", "Team_PPG"]]
        .rename(columns={
            "Season_Years":      "Season",
            "Team_Name":         "Team",
            "Team_Abbreviation": "Abbr",
            "Team_Conference":   "Conference",
            "Team_PPG":          "PPG",
        })
        .reset_index(drop=True)   # resets row index to 0,1,2... after filtering/sorting
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,          # don't show the numeric row index column
        column_config={
            # format the PPG column to always display exactly 2 decimal places
            "PPG": st.column_config.NumberColumn(format="%.2f")
        },
    )