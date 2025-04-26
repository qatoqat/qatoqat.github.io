base = "templates/base.html"
destination = "public/index.html"

title = "Home"

styles = [
    "/assets/css/home.css",
]

scripts = [
    "/assets/js/discord.js",
    "/assets/js/github.js",
]

content = """
<a id="banner" href="/assets/img/banner-full.png">
    <img src="/assets/img/banner-3-1.png" alt="Banner art by Plidgey on ArtFight">
    <span>Art by Plidgey on ArtFight</span>
</a>
<div id="container">
    <div id="content">
        <div class="card">
            <h2>Welcome, travellers . . .</h2>
            <p>
                Hello! It's Qato/Qatoqat (pronounced catto/catto-cat).
                I make pixel art, digital illustrations, apps and games.
                You will find mostly cat-themed artwork from me.
                Be sure to check out the news and other sections.
                Hope you enjoy your visit! =ω=
            </p>
        </div>
        <div class="card">
            <h2>Latest</h2>
            <p>
                No content available yet
            </p>
        </div>
        <div class="card">
            <h2>Featured</h2>
            <p>
                No content available yet
            </p>
        </div>
    </div>
    <div id="sidebar">
        <a class="item commission" href="https://bsky.app/profile/qatoqat.bsky.social">
            <span>Commission status</span>
            <span id="commission-status">ASK ME!</span>
        </a>
        <a class="item discord" href="https://discord.gg/bSDPbbdkCb">
            <span>Join our server on</span>
            <img src="/assets/img/discord-logo.png" alt="Discord logo">
            <span id="online-status"><i class="indicator yellow"></i> connecting </span>
        </a>
        <a class="item kofi" href="https://ko-fi.com/qatoqat">
            <span>Support us on</span>
            <img src="/assets/img/kofi-logo.png" alt="Ko-fi logo">
        </a>
    </div>
</div>
<div id="links">
    <a href="https://bsky.app/profile/qatoqat.bsky.social" class="has-tooltip">
        <div><i class="fa-brands fa-bluesky"></i></div>
        <span class="tooltip bottom">Bluesky</span>
    </a>
    <a href="https://twitter.com/qatoqat" class="has-tooltip">
        <div><i class="fa-brands fa-twitter"></i></div>
        <span class="tooltip bottom">Twitter</span>
    </a>
    <a href="https://discord.gg/bSDPbbdkCb" class="has-tooltip">
        <div><i class="fa-brands fa-discord"></i></div>
        <span class="tooltip bottom">Discord</span>
    </a>
    <a href="https://www.youtube.com/channel/UCYhx1kQUT7hEPZM7RlOnsEw" class="has-tooltip">
        <div><i class="fa-brands fa-youtube"></i></div>
        <span class="tooltip bottom">YouTube</span>
    </a>
    <a href="https://ko-fi.com/qatoqat" class="has-tooltip">
        <div><img src="/assets/img/kofi-icon.png" alt="Ko-fi icon"></div>
        <span class="tooltip bottom">Ko-fi</span>
    </a>
    <a href="https://patreon.com/c/qatoqat" class="has-tooltip">
        <div><i class="fa-brands fa-patreon"></i></div>
        <span class="tooltip bottom">Patreon (Ko-fi preferred)</span>
    </a>
    <a href="https://www.pixiv.net/en/users/66979978" class="has-tooltip">
        <div><i class="fa-brands fa-pixiv"></i></div>
        <span class="tooltip bottom">Pixiv</span>
    </a>
    <a href="https://qatoqat.itch.io" class="has-tooltip">
        <div><i class="fa-brands fa-itch-io"></i></div>
        <span class="tooltip bottom">itch.io</span>
    </a>
    <a href="https://github.com/qatoqat" class="has-tooltip">
        <div><i class="fa-brands fa-github"></i></div>
        <span class="tooltip bottom">GitHub</span>
    </a>
</div>
"""
