import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import numpy as np

# ============================================
# DATA FOR EACH JOB ROLE
# ============================================

# 1. HPC Solutions Architect
solutions_architect = {
    'foundation': [
        ("Cluster Management", 25),
        ("GPU & Accelerated Computing", 19),
        ("Networking & Infrastructure", 17),
        ("Performance Optimization", 16),
        ("Storage & Data Management", 15),
    ],
    'mid': [
        ("Containerization & Orchestration", 14),
        ("Automation", 12),
        ("Cloud Computing", 10),
        ("Project & Team Leadership", 9),
        ("Security & Compliance", 8),
        ("Coding & Software Development", 8),
        ("Monitoring & Observability", 7),
    ],
    'peak': [
        ("Research Computing Support", 6),
        ("User Support & Training", 5),
        ("Database & Application Management", 3),
    ]
}

# 2. HPC Systems Engineer
systems_engineer = {
    'foundation': [
        ("Cluster Management", 189),
        ("Performance Optimization", 85),
        ("Networking & Infrastructure", 82),
        ("GPU & Accelerated Computing", 80),
        ("Storage & Data Management", 78),
    ],
    'mid': [
        ("Automation", 70),
        ("Containerization & Orchestration", 65),
        ("Monitoring & Observability", 55),
        ("Cloud Computing", 48),
        ("Security & Compliance", 40),
        ("Coding & Software Development", 38),
    ],
    'peak': [
        ("User Support & Training", 35),
        ("Research Computing Support", 30),
        ("Project & Team Leadership", 28),
        ("Database & Application Management", 15),
    ]
}

# 3. HPC Software Engineer
software_engineer = {
    'foundation': [
        ("Coding & Software Development", 20),
        ("GPU & Accelerated Computing", 18),
        ("Performance Optimization", 18),
        ("Cluster Management", 16),
    ],
    'mid': [
        ("Research Computing Support", 12),
        ("Automation", 10),
        ("Containerization & Orchestration", 9),
        ("Monitoring & Observability", 8),
    ],
    'peak': [
        ("Networking & Infrastructure", 7),
        ("Storage & Data Management", 7),
        ("Cloud Computing", 6),
        ("Security & Compliance", 5),
        ("Database & Application Management", 5),
        ("Project & Team Leadership", 4),
        ("User Support & Training", 3),
    ]
}

# 4. HPC Technical Leader
tech_leader = {
    'foundation': [
        ("Cluster Management", 13),
        ("Networking & Infrastructure", 7),
        ("Performance Optimization", 7),
    ],
    'mid': [
        ("Project & Team Leadership", 8),
        ("GPU & Accelerated Computing", 6),
        ("Storage & Data Management", 6),
        ("Automation", 6),
        ("Security & Compliance", 5),
        ("Cloud Computing", 5),
        ("Containerization & Orchestration", 5),
    ],
    'peak': [
        ("Monitoring & Observability", 4),
        ("Research Computing Support", 3),
        ("User Support & Training", 2),
        ("Database & Application Management", 2),
        ("Coding & Software Development", 1),
    ]
}

# ============================================
# PYRAMID DRAWING FUNCTION
# ============================================

def draw_substack_pyramid(data, title, subtitle, filename, colors=None):
    """
    Draw a beautiful pyramid diagram optimized for Substack articles.
    
    Parameters:
    - data: dict with 'foundation', 'mid', 'peak' keys
    - title: Main title string
    - subtitle: Subtitle string
    - filename: Output filename (PNG)
    - colors: dict with 'foundation', 'mid', 'peak' hex colors
    """
    
    if colors is None:
        colors = {
            'foundation': '#0C2340',    # Deep navy
            'mid': '#1A5276',           # Medium blue
            'peak': '#5DADE2'           # Light blue
        }
    
    # Substack optimal size
    fig_width = 14
    fig_height = 12
    
    fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
    
    # Set background to white (Substack standard)
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(0, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Level configuration
    level_configs = [
        ('foundation', 0.0, 0.50, colors['foundation'], '🥾 FOUNDATION', 16, '#FFFFFF'),
        ('mid', 0.50, 0.78, colors['mid'], '📈 MID-LEVEL', 14, '#FFFFFF'),
        ('peak', 0.78, 1.02, colors['peak'], '🚀 PEAK', 12, '#0C2340')
    ]
    
    y_position = 0.0
    
    for level_key, y_start, y_end, color, label, fontsize, text_color in level_configs:
        items = data.get(level_key, [])
        if not items:
            continue
            
        height = y_end - y_start
        total_count = sum(count for _, count in items)
        max_width = 0.95
        
        # Calculate item heights within the level
        item_height = (height * 0.85) / len(items)
        gap = (height * 0.15) / (len(items) + 1)
        
        for i, (name, count) in enumerate(items):
            # Width proportional to count, with minimum width
            width_ratio = count / total_count if total_count > 0 else 0
            item_width = max_width * (0.35 + 0.65 * width_ratio)
            
            # Trapezoid gets narrower toward the top
            bottom_width = item_width
            top_width = item_width * 0.80
            
            x_center = 0
            y_bottom = y_position + gap + i * (item_height + gap)
            y_top = y_bottom + item_height
            
            # Create trapezoid
            trapezoid = Polygon(
                [
                    (-bottom_width/2, y_bottom),
                    (bottom_width/2, y_bottom),
                    (top_width/2, y_top),
                    (-top_width/2, y_top)
                ],
                closed=True,
                facecolor=color,
                edgecolor='#FFFFFF',
                linewidth=2,
                alpha=0.7 + 0.3 * width_ratio
            )
            ax.add_patch(trapezoid)
            
            # Add shadow effect (subtle)
            shadow = Polygon(
                [
                    (-bottom_width/2 - 0.005, y_bottom - 0.005),
                    (bottom_width/2 + 0.005, y_bottom - 0.005),
                    (top_width/2 + 0.005, y_top - 0.005),
                    (-top_width/2 - 0.005, y_top - 0.005)
                ],
                closed=True,
                facecolor='#000000',
                alpha=0.05
            )
            ax.add_patch(shadow)
            
            # Determine text color based on background
            if level_key == 'peak':
                txt_color = '#0C2340'
            else:
                txt_color = '#FFFFFF'
            
            # Skill name
            fontsize_name = 11 if len(name) > 20 else 13
            ax.text(
                x_center, (y_bottom + y_top) / 2 + 0.01,
                name,
                ha='center', va='center',
                fontsize=fontsize_name,
                fontweight='bold',
                color=txt_color,
                wrap=True
            )
            
            # Count
            ax.text(
                x_center, (y_bottom + y_top) / 2 - 0.03,
                f'({count})',
                ha='center', va='center',
                fontsize=fontsize_name - 2,
                color=txt_color,
                alpha=0.8
            )
        
        # Level label on the left
        ax.text(
            -1.08, (y_start + y_end) / 2,
            label,
            ha='center', va='center',
            fontsize=fontsize,
            fontweight='bold',
            color=color,
            rotation=90
        )
        
        y_position = y_end
    
    # Title
    ax.text(
        0, 1.10,
        title,
        ha='center', va='center',
        fontsize=24,
        fontweight='bold',
        color='#0C2340'
    )
    
    # Subtitle
    ax.text(
        0, 1.055,
        subtitle,
        ha='center', va='center',
        fontsize=14,
        color='#555555',
        fontstyle='italic'
    )
    
    # Footer / data source
    ax.text(
        0, -0.02,
        'Source: HPC Job Postings Analysis (2026) · Frequency indicates occurrence in job descriptions',
        ha='center', va='center',
        fontsize=10,
        color='#999999',
        fontstyle='italic'
    )
    
    plt.tight_layout()
    plt.savefig(
        filename,
        dpi=300,
        bbox_inches='tight',
        facecolor='#FFFFFF',
        edgecolor='none'
    )
    plt.close()
    
    print(f"✅ Saved: {filename}")

# ============================================
# GENERATE ALL FOUR PYRAMIDS
# ============================================

# Custom color schemes (optimized for Substack)
color_schemes = {
    'default': {
        'foundation': '#0C2340',
        'mid': '#1A5276',
        'peak': '#5DADE2'
    },
    'warm': {
        'foundation': '#7B2D26',
        'mid': '#A04037',
        'peak': '#E8A598'
    },
    'tech': {
        'foundation': '#0D47A1',
        'mid': '#1976D2',
        'peak': '#64B5F6'
    }
}

# Generate pyramids
draw_substack_pyramid(
    solutions_architect,
    'HPC Solutions Architect',
    'Skills Relevance Pyramid',
    'hpc_solutions_architect_pyramid.png',
    color_schemes['default']
)

draw_substack_pyramid(
    systems_engineer,
    'HPC Systems Engineer',
    'Skills Relevance Pyramid',
    'hpc_systems_engineer_pyramid.png',
    color_schemes['default']
)

draw_substack_pyramid(
    software_engineer,
    'HPC Software Engineer',
    'Skills Relevance Pyramid',
    'hpc_software_engineer_pyramid.png',
    color_schemes['default']
)

draw_substack_pyramid(
    tech_leader,
    'HPC Technical Leader',
    'Skills Relevance Pyramid',
    'hpc_technical_leader_pyramid.png',
    color_schemes['default']
)

print("\n✅ All pyramids generated successfully!")
print("📁 Files created:")
print("   - hpc_solutions_architect_pyramid.png")
print("   - hpc_systems_engineer_pyramid.png")
print("   - hpc_software_engineer_pyramid.png")
print("   - hpc_technical_leader_pyramid.png")
