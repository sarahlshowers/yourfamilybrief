#!/usr/bin/env node
// Regenerates the auto-generated block in blog.html from posts/posts.json.
// Run manually with `node scripts/build-blog.js`, or let Vercel run it on deploy
// (see vercel.json buildCommand).

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const POSTS_JSON = path.join(ROOT, 'posts', 'posts.json');
const BLOG_HTML = path.join(ROOT, 'blog.html');

const START = '<!-- BLOG-INDEX:START -->';
const END = '<!-- BLOG-INDEX:END -->';

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function formatDate(iso) {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

const posts = JSON.parse(fs.readFileSync(POSTS_JSON, 'utf8'));
if (posts.length === 0) {
  throw new Error('posts/posts.json has no entries');
}

posts.sort((a, b) => b.date.localeCompare(a.date));
const [latest, ...rest] = posts;

const heroBlock = `  <a class="hero" href="posts/${latest.slug}.html">
    <p class="hero-label">Latest</p>
    <h1>${escapeHtml(latest.title)}</h1>
    <p>${escapeHtml(latest.dek)}</p>
  </a>

  <div class="hairline"></div>

  <div class="post-list">
`;

const cards = rest
  .map(
    (p) => `    <a class="post-card" href="posts/${p.slug}.html">
      <div>
        <div class="post-tag">${escapeHtml(p.tag)}</div>
        <div class="post-title">${escapeHtml(p.title)}</div>
        <p class="post-excerpt">${escapeHtml(p.dek)}</p>
      </div>
      <div class="post-meta">
        <span class="post-date">${formatDate(p.date)}</span>
        <span class="read-time">${escapeHtml(p.readTime)}</span>
      </div>
    </a>`
  )
  .join('\n\n');

const block = `${START}\n${heroBlock}${cards}\n\n  </div>\n  ${END}`;

const html = fs.readFileSync(BLOG_HTML, 'utf8');
const startIdx = html.indexOf(START);
const endIdx = html.indexOf(END);
if (startIdx === -1 || endIdx === -1) {
  throw new Error('blog.html is missing BLOG-INDEX:START / BLOG-INDEX:END markers');
}

const before = html.slice(0, startIdx);
const after = html.slice(endIdx + END.length);
fs.writeFileSync(BLOG_HTML, before + block + after);

console.log(`blog.html regenerated: ${posts.length} posts (latest: ${latest.slug}, ${latest.date})`);
