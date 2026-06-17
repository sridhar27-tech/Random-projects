const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');
const cors = require('@koa/cors');
const fs = require('fs/promises');
const path = require('path');

const app = new Koa();
const router = new Router();

app.use(cors());
app.use(bodyParser());

// Load data
const getData = async () => {
  const dataPath = path.join(__dirname, 'data.json');
  const data = await fs.readFile(dataPath, 'utf-8');
  return JSON.parse(data);
};

// Routes
router.get('/', async (ctx) => {
  ctx.body = {
    message: 'Spotify Clone API is running',
    endpoints: ['/api/songs', '/api/playlists']
  };
});

// Routes
router.get('/api/songs', async (ctx) => {
  try {
    const songs = await getData();
    ctx.body = songs;
  } catch (err) {
    ctx.status = 500;
    ctx.body = { error: 'Failed to fetch songs' };
  }
});

// Mock database for playlists
let playlists = [
  { id: 'p1', name: 'My Awesome Playlist #1', songs: ['1', '2'] },
  { id: 'p2', name: 'Workout Mix', songs: ['3'] }
];

router.get('/api/playlists', async (ctx) => {
  ctx.body = playlists;
});

router.post('/api/playlists', async (ctx) => {
  const { name } = ctx.request.body;
  const newPlaylist = {
    id: `p${playlists.length + 1}`,
    name: name || `My Playlist #${playlists.length + 1}`,
    songs: []
  };
  playlists.push(newPlaylist);
  ctx.status = 201;
  ctx.body = newPlaylist;
});

app.use(router.routes()).use(router.allowedMethods());

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
