<svg xmlns="http://w3.org" viewBox="0 0 1180 610" width="100%" height="100%">
  <defs>
    <linearGradient id="dark-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030712"/>
      <stop offset="50%" stop-color="#0b0f19"/>
      <stop offset="100%" stop-color="#030712"/>
    </linearGradient>
    <linearGradient id="accent-grad-dark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="50%" stop-color="#22D3EE"/>
      <stop offset="100%" stop-color="#10B981"/>
      <animate attributeName="y1" values="0%;50%;0%" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="ascii-grad-dark" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="50%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#10B981"/>
      <animate attributeName="x1" values="0%;100%;0%" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="glow-dark" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <style>
      .bg { fill: url(#dark-bg-grad); }
      .panel { fill: #0F172A; stroke: rgba(255,255,255,0.08); stroke-width: 1; rx: 16px; }
      .text-main { fill: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace; font-size: 14px; }
      .text-muted { fill: #94A3B8; font-family: monospace; font-size: 12px; }
      .cursor { fill: #22D3EE; animation: blink 1s infinite; }
      @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
      .pill { fill: rgba(30, 41, 59, 0.7); stroke: rgba(255,255,255,0.1); rx: 8px; transition: all 0.3s ease; }
      .pill:hover { stroke: #22D3EE; filter: drop-shadow(0 0 8px rgba(34,211,238,0.5)); transform: scale(1.05); }
    </style>
  </defs>
  <rect width="1180" height="610" rx="20" class="bg"/>
  <!-- Ambient background glow -->
  <circle cx="200" cy="150" r="180" fill="#7C3AED" opacity="0.15" filter="url(#glow-dark)"/>
  <circle cx="900" cy="450" r="220" fill="#22D3EE" opacity="0.1" filter="url(#glow-dark)"/>
  
  <!-- Left Side Panel (ASCII Portrait) -->
  <rect x="30" y="30" width="418" height="550" class="panel"/>
  <g transform="translate(50, 60)">
    <text x="0" y="20" fill="url(#ascii-grad-dark)" font-family="monospace" font-size="9" font-weight="bold">
      <tspan x="0" dy="0">    .---.    </tspan>
      <tspan x="0" dy="12">   /     \   </tspan>
      <tspan x="0" dy="12">  | () () |  </tspan>
      <tspan x="0" dy="12">   \  _  /   </tspan>
      <tspan x="0" dy="12">    `---`    </tspan>
      <tspan x="0" dy="12">  CYBER_DEV  </tspan>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-6; 0,0" dur="4s" repeatCount="indefinite"/>
    </text>
  </g>

  <!-- Right Side Panel (Terminal) -->
  <rect x="478" y="30" width="672" height="550" class="panel"/>
  <g transform="translate(518, 80)">
    <text x="0" y="0" class="text-main" font-size="20" font-weight="bold">Hi 👋 I'm <tspan fill="url(#accent-grad-dark)">Developer</tspan></text>
    <text x="0" y="35" class="text-muted">> building digital experiences...</text>
    <!-- Metadata rows -->
    <text x="0" y="80" class="text-main">📍 Location: <tspan class="text-muted">Earth / Remote</tspan></text>
    <text x="0" y="110" class="text-main">🎓 Education: <tspan class="text-muted">Computer Science</tspan></text>
    <text x="0" y="140" class="text-main">🚀 Focus: <tspan class="text-muted">AI &amp; High-Performance Web</tspan></text>
    
    <!-- Skills Grid / Pills -->
    <g transform="translate(0, 180)">
      <rect x="0" y="0" width="80" height="30" class="pill"/><text x="15" y="20" class="text-muted" fill="#F8FAFC">React</text>
      <rect x="90" y="0" width="90" height="30" class="pill"/><text x="105" y="20" class="text-muted" fill="#F8FAFC">Next.js</text>
      <rect x="190" y="0" width="80" height="30" class="pill"/><text x="205" y="20" class="text-muted" fill="#F8FAFC">Node.js</text>
      <rect x="280" y="0" width="95" height="30" class="pill"/><text x="295" y="20" class="text-muted" fill="#F8FAFC">TypeScript</text>
      
      <rect x="0" y="40" width="85" height="30" class="pill"/><text x="15" y="60" class="text-muted" fill="#F8FAFC">Tailwind</text>
      <rect x="95" y="40" width="80" height="30" class="pill"/><text x="110" y="60" class="text-muted" fill="#F8FAFC">Python</text>
      <rect x="185" y="40" width="85" height="30" class="pill"/><text x="200" y="60" class="text-muted" fill="#F8FAFC">Docker</text>
      <rect x="280" y="40" width="90" height="30" class="pill"/><text x="295" y="60" class="text-muted" fill="#F8FAFC">Postgres</text>
    </g>
  </g>
</svg>
