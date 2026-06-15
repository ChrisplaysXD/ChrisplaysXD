import os

def create_pixel_path(grid_str, color_map, pixel_size=3):
    """
    Converts a grid string into SVG rects.
    Using <rect> for simplicity and crisp rendering.
    """
    rows = grid_str.strip().split('\n')
    rects = []
    for y, row in enumerate(rows):
        cols = row.split()
        for x, val in enumerate(cols):
            if val in color_map and val != '.':
                color = color_map[val]
                px = x * pixel_size
                py = y * pixel_size
                rects.append(f'<rect x="{px}" y="{py}" width="{pixel_size}" height="{pixel_size}" fill="{color}" shape-rendering="crispEdges" />')
    return '\n'.join(rects)

# Sprite 1: Hacker standing/running (Frame A)
hacker_grid_a = """
. . . . . G G G G G . . . . .
. . . . G G G G G G G . . . .
. . . G G D D D D G G G . . .
. . G G D W . . W D G G . . .
. . G G D . . . . D G G . . .
. . G G D D D D D D G G . . .
. . . G G G G G G G G . . . .
. . . . D D D D D D . . . . .
. . . D D D D D D D D . . . .
. . G D D D D D D D D G . . .
. G G D D D D D D D D G G . .
. G G D D D D D D D D G G . .
. . . D D D D D D D D . . . .
. . . D D . . . . D D . . . .
. . D D . . . . . . D D . . .
. D D D . . . . . . D D D . .
"""

# Sprite 2: Hacker running (Frame B - legs alternate)
hacker_grid_b = """
. . . . . G G G G G . . . . .
. . . . G G G G G G G . . . .
. . . G G D D D D G G G . . .
. . G G D W . . W D G G . . .
. . G G D . . . . D G G . . .
. . G G D D D D D D G G . . .
. . . G G G G G G G G . . . .
. . . . D D D D D D . . . . .
. . . D D D D D D D D . . . .
. . G D D D D D D D D G . . .
. G G D D D D D D D D G G . .
. G G D D D D D D D D G G . .
. . . D D D D D D D D . . . .
. . . . D D . . D D . . . . .
. . . . . D D . D D . . . . .
. . . . D D D . D D D . . . .
"""

# Sprite 3: Red Firewall Obstacle
firewall_grid = """
. . R R R R R R R R R R . .
. R R O O O O O O O O R R .
R R O O O O O O O O O O R R
R O O R R R R R R R R O O R
R O R R . . . . . . R R O R
R O R . . . . . . . . R O R
R O R . . X X X X . . R O R
R O R . . X . . X . . R O R
R O R . . X X X X . . R O R
R O R . . . . X . . . R O R
R O R . . . . X . . . R O R
R O O R R R R R R R R O O R
R R O O O O O O O O O O R R
. R R O O O O O O O O R R .
. . R R R R R R R R R R . .
"""

# Sprite 4: Green Bug/Virus (chased in footer)
bug_grid = """
. V . . . . . . V .
. . V . . . . V . .
. . V V V V V V . .
. V V X V V X V V .
V V V V V V V V V V
V V V V V V V V V V
. V V V V V V V V .
. . V . V . V . V .
. V . . V . . V . .
"""

color_map = {
    'G': '#00ff41', # Neon green hoodie
    'D': '#161b22', # Dark coat
    'W': '#58a6ff', # Blue glowing eyes
    'R': '#ff4c4c', # Red firewall outline
    'O': '#ff9f1a', # Orange firewall fill
    'X': '#ffffff', # White lock center
    'V': '#ea4aaa', # Pink/Magenta virus
}

# Compile sprites
hacker_a_svg = create_pixel_path(hacker_grid_a, color_map, pixel_size=3)
hacker_b_svg = create_pixel_path(hacker_grid_b, color_map, pixel_size=3)
firewall_svg = create_pixel_path(firewall_grid, color_map, pixel_size=3)
bug_svg = create_pixel_path(bug_grid, color_map, pixel_size=3)

# 1. Top Banner SVG
top_banner_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 180" width="100%" height="100%">
  <style>
    <![CDATA[
    .bg {{
      fill: #0b0e14;
    }}
    .grid {{
      stroke: #161b22;
      stroke-width: 0.5;
    }}
    .ground {{
      stroke: #00ff41;
      stroke-width: 2;
      stroke-dasharray: 4 4;
    }}
    
    /* Animation for hacker jumping and running */
    @keyframes runner-switch {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @keyframes runner-switch-inv {{
      0%, 49% {{ opacity: 0; }}
      50%, 100% {{ opacity: 1; }}
    }}
    
    @keyframes jump {{
      0% {{ transform: translateY(0); }}
      /* Run-up */
      65% {{ transform: translateY(0); }}
      /* Jump up */
      72% {{ transform: translateY(-70px); }}
      /* Peak */
      76% {{ transform: translateY(-70px); }}
      /* Land */
      83% {{ transform: translateY(0); }}
      100% {{ transform: translateY(0); }}
    }}

    @keyframes scroll-obstacle {{
      0% {{ transform: translateX(850px); }}
      100% {{ transform: translateX(-100px); }}
    }}

    @keyframes scroll-bg {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-40px); }}
    }}

    .hacker-container {{
      animation: jump 4s infinite cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}

    .frame-a {{
      animation: runner-switch 0.3s infinite;
    }}
    .frame-b {{
      animation: runner-switch-inv 0.3s infinite;
    }}

    .obstacle {{
      animation: scroll-obstacle 4s infinite linear;
    }}

    .star-bg {{
      animation: scroll-bg 8s infinite linear;
    }}

    .glow-text {{
      font-family: 'Courier New', Courier, monospace;
      font-weight: bold;
      fill: #00ff41;
      text-shadow: 0 0 5px #00ff41;
    }}

    .binary-text {{
      font-family: monospace;
      font-size: 10px;
      fill: #161b22;
    }}
    ]]>
  </style>

  <!-- Background -->
  <rect width="800" height="180" class="bg" />

  <!-- Background Grid -->
  <g class="star-bg">
    <line x1="0" y1="20" x2="1600" y2="20" class="grid" />
    <line x1="0" y1="40" x2="1600" y2="40" class="grid" />
    <line x1="0" y1="60" x2="1600" y2="60" class="grid" />
    <line x1="0" y1="80" x2="1600" y2="80" class="grid" />
    <line x1="0" y1="100" x2="1600" y2="100" class="grid" />
    <line x1="0" y1="120" x2="1600" y2="120" class="grid" />
    <line x1="0" y1="140" x2="1600" y2="140" class="grid" />
    
    <!-- Vertical Grid Lines -->
    <line x1="0" y1="0" x2="0" y2="150" class="grid" />
    <line x1="40" y1="0" x2="40" y2="150" class="grid" />
    <line x1="80" y1="0" x2="80" y2="150" class="grid" />
    <line x1="120" y1="0" x2="120" y2="150" class="grid" />
    <line x1="160" y1="0" x2="160" y2="150" class="grid" />
    <line x1="200" y1="0" x2="200" y2="150" class="grid" />
    <line x1="240" y1="0" x2="240" y2="150" class="grid" />
    <line x1="280" y1="0" x2="280" y2="150" class="grid" />
    <line x1="320" y1="0" x2="320" y2="150" class="grid" />
    <line x1="360" y1="0" x2="360" y2="150" class="grid" />
    <line x1="400" y1="0" x2="400" y2="150" class="grid" />
    <line x1="440" y1="0" x2="440" y2="150" class="grid" />
    <line x1="480" y1="0" x2="480" y2="150" class="grid" />
    <line x1="520" y1="0" x2="520" y2="150" class="grid" />
    <line x1="560" y1="0" x2="560" y2="150" class="grid" />
    <line x1="600" y1="0" x2="600" y2="150" class="grid" />
    <line x1="640" y1="0" x2="640" y2="150" class="grid" />
    <line x1="680" y1="0" x2="680" y2="150" class="grid" />
    <line x1="720" y1="0" x2="720" y2="150" class="grid" />
    <line x1="760" y1="0" x2="760" y2="150" class="grid" />
    <line x1="800" y1="0" x2="800" y2="150" class="grid" />
    <line x1="840" y1="0" x2="840" y2="150" class="grid" />
  </g>

  <!-- Binary Background Noise -->
  <text x="30" y="30" class="binary-text">01000011 01011001</text>
  <text x="550" y="35" class="binary-text">01010011 01000101 01000011</text>
  <text x="180" y="55" class="binary-text">10010110 11011010</text>
  <text x="400" y="45" class="binary-text">01101100 01101001 01101110 01110101 01111000</text>

  <!-- Ground Line -->
  <line x1="0" y1="150" x2="800" y2="150" class="ground" />

  <!-- Animated Obstacle (Firewall) -->
  <g class="obstacle" transform="translate(0, 105)">
    {firewall_svg}
    <text x="0" y="-10" font-family="monospace" font-size="9" fill="#ff4c4c" font-weight="bold">PORT 80</text>
  </g>

  <!-- Animated Hacker -->
  <g class="hacker-container" transform="translate(180, 102)">
    <g class="frame-a">
      {hacker_a_svg}
    </g>
    <g class="frame-b" style="display: none;">
      <!-- CSS runner-switch overrides display: none -->
      {hacker_b_svg}
    </g>
    <!-- Little status label -->
    <text x="-15" y="-12" font-family="monospace" font-size="9" fill="#00ff41">chris@sec</text>
  </g>

  <!-- Overlay Header Text -->
  <rect x="250" y="65" width="300" height="50" fill="#0b0e14" opacity="0.8" rx="5" />
  <text x="400" y="95" class="glow-text" font-size="20" text-anchor="middle">🔒 CHRIS // SECURITY</text>
  <text x="400" y="110" font-family="monospace" font-size="10" fill="#8b949e" text-anchor="middle">Status: Escaping Firewalls...</text>
</svg>
"""

# 2. Bottom Banner SVG
bottom_banner_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 100" width="100%" height="100%">
  <style>
    .bg {{
      fill: #0b0e14;
    }}
    .ground {{
      stroke: #00ff41;
      stroke-width: 2;
      stroke-dasharray: 4 4;
    }}
    
    @keyframes runner-switch {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @keyframes runner-switch-inv {{
      0%, 49% {{ opacity: 0; }}
      50%, 100% {{ opacity: 1; }}
    }}

    @keyframes chase-bug {{
      0% {{ transform: translateX(850px); }}
      100% {{ transform: translateX(-100px); }}
    }}

    @keyframes jump-hacker {{
      0% {{ transform: translateY(0); }}
      10% {{ transform: translateY(0); }}
      15% {{ transform: translateY(-20px); }}
      20% {{ transform: translateY(0); }}
      100% {{ transform: translateY(0); }}
    }}

    .bug {{
      animation: chase-bug 6s infinite linear;
    }}

    .hacker-container {{
      animation: jump-hacker 2s infinite ease-in-out;
    }}

    .frame-a {{
      animation: runner-switch 0.2s infinite;
    }}
    .frame-b {{
      animation: runner-switch-inv 0.2s infinite;
    }}

    .footer-text {{
      font-family: 'Courier New', Courier, monospace;
      font-weight: bold;
      fill: #8b949e;
      font-size: 11px;
    }}
  </style>

  <!-- Background -->
  <rect width="800" height="100" class="bg" />

  <!-- Ground Line -->
  <line x1="0" y1="80" x2="800" y2="80" class="ground" />

  <!-- The Bug/Virus being chased -->
  <g class="bug" transform="translate(0, 50)">
    {bug_svg}
    <text x="-10" y="-8" font-family="monospace" font-size="8" fill="#ea4aaa">virus.exe</text>
  </g>

  <!-- Hacker chasing -->
  <g transform="translate(250, 32)">
    <g class="hacker-container">
      <g class="frame-a">
        {hacker_a_svg}
      </g>
      <g class="frame-b">
        {hacker_b_svg}
      </g>
    </g>
    <text x="-15" y="-10" font-family="monospace" font-size="8" fill="#00ff41">hunting...</text>
  </g>

  <!-- Footer text decoration -->
  <text x="20" y="30" class="footer-text">> systemctl status threat-hunting.service</text>
  <text x="20" y="45" font-family="monospace" font-size="10" fill="#00ff41">● active (running) - Hunt in progress</text>
  
  <text x="780" y="30" class="footer-text" text-anchor="end">EST. 2026</text>
</svg>
"""

# Write files
os.makedirs('/home/chrisplaysxd/ChrisplaysXD/assets', exist_ok=True)
with open('/home/chrisplaysxd/ChrisplaysXD/assets/cyber_header.svg', 'w') as f:
    f.write(top_banner_content)
with open('/home/chrisplaysxd/ChrisplaysXD/assets/cyber_footer.svg', 'w') as f:
    f.write(bottom_banner_content)

print("Banners generated successfully!")
