const MODELS_KEY = 'yonocytech_models';
const REQUESTS_KEY = 'yonocytech_requests';

function getModels() {
  return JSON.parse(localStorage.getItem(MODELS_KEY) || '[]');
}

function saveModels(models) {
  localStorage.setItem(MODELS_KEY, JSON.stringify(models));
}

function getRequestLog() {
  return JSON.parse(localStorage.getItem(REQUESTS_KEY) || '[]');
}

const DEFAULT_MODELS = [
  { id: 'openrouter', name: 'OpenRouter (Primary)', provider: 'OpenRouter', status: 'active', rateLimit: 30, priority: 1, apiKeySet: true },
  { id: 'huggingface', name: 'HuggingFace Inference', provider: 'HuggingFace', status: 'active', rateLimit: 20, priority: 2, apiKeySet: true },
  { id: 'github-models', name: 'GitHub Models (Azure)', provider: 'GitHubModels', status: 'active', rateLimit: 25, priority: 3, apiKeySet: true },
  { id: 'deepai', name: 'DeepAI Image Gen', provider: 'DeepAI', status: 'active', rateLimit: 10, priority: 4, apiKeySet: false }
];

const DEFAULT_AGENTS = [
  { id: 'coding', name: 'Coding Agent', icon: '💻', status: 'active', model: 'openrouter', priority: 1 },
  { id: 'writing', name: 'Writing Agent', icon: '✍️', status: 'active', model: 'openrouter', priority: 2 },
  { id: 'data', name: 'Data Agent', icon: '📊', status: 'active', model: 'huggingface', priority: 3 },
  { id: 'design', name: 'Design Agent', icon: '🎨', status: 'active', model: 'openrouter', priority: 4 },
  { id: 'marketing', name: 'Marketing Agent', icon: '📈', status: 'active', model: 'openrouter', priority: 5 },
  { id: 'research', name: 'Research Agent', icon: '🔍', status: 'active', model: 'huggingface', priority: 6 }
];

function initModels() {
  if (!localStorage.getItem(MODELS_KEY)) {
    saveModels(DEFAULT_MODELS);
  }
  if (!localStorage.getItem('yonocytech_agents')) {
    localStorage.setItem('yonocytech_agents', JSON.stringify(DEFAULT_AGENTS));
  }
}

function getAgents() {
  return JSON.parse(localStorage.getItem('yonocytech_agents') || '[]');
}

function saveAgents(agents) {
  localStorage.setItem('yonocytech_agents', JSON.stringify(agents));
}

function toggleModelStatus(modelId) {
  const models = getModels();
  const model = models.find(m => m.id === modelId);
  if (model) {
    model.status = model.status === 'active' ? 'limited' : model.status === 'limited' ? 'off' : 'active';
    saveModels(models);
    renderModelTable();
    renderAgentStatus();
  }
}

function toggleAgentStatus(agentId) {
  const agents = getAgents();
  const agent = agents.find(a => a.id === agentId);
  if (agent) {
    agent.status = agent.status === 'active' ? 'limited' : agent.status === 'limited' ? 'off' : 'active';
    saveAgents(agents);
    renderAgentTable();
  }
}

function renderModelTable() {
  const tbody = document.getElementById('modelTableBody');
  if (!tbody) return;
  const models = getModels();
  tbody.innerHTML = models.map(m => {
    const statusClass = m.status === 'active' ? 'status-active' : m.status === 'limited' ? 'status-limited' : 'status-off';
    const statusLabel = m.status === 'active' ? 'Active' : m.status === 'limited' ? 'Limited' : 'Disabled';
    return `<tr>
      <td style="color:var(--text);font-weight:600;">${m.name}</td>
      <td>${m.provider}</td>
      <td>${m.rateLimit}/min</td>
      <td><span class="status-badge ${statusClass}">${statusLabel}</span></td>
      <td>${m.apiKeySet ? '✅' : '❌'}</td>
      <td>
        <label class="toggle-switch">
          <input type="checkbox" ${m.status === 'active' ? 'checked' : ''} onchange="toggleModelStatus('${m.id}')" />
          <span class="toggle-slider"></span>
        </label>
      </td>
    </tr>`;
  }).join('');
}

function renderAgentTable() {
  const tbody = document.getElementById('agentTableBody');
  if (!tbody) return;
  const agents = getAgents();
  tbody.innerHTML = agents.map(a => {
    const statusClass = a.status === 'active' ? 'status-active' : a.status === 'limited' ? 'status-limited' : 'status-off';
    const statusLabel = a.status === 'active' ? 'Active' : a.status === 'limited' ? 'Limited' : 'Disabled';
    return `<tr>
      <td style="color:var(--text);font-weight:600;">${a.icon} ${a.name}</td>
      <td>${a.model}</td>
      <td><span class="status-badge ${statusClass}">${statusLabel}</span></td>
      <td>
        <label class="toggle-switch">
          <input type="checkbox" ${a.status === 'active' ? 'checked' : ''} onchange="toggleAgentStatus('${a.id}')" />
          <span class="toggle-slider"></span>
        </label>
      </td>
    </tr>`;
  }).join('');
}

function renderAgentStatus() {
  const container = document.getElementById('agentStatusCards');
  if (!container) return;
  const agents = getAgents();
  const models = getModels();
  container.innerHTML = agents.map(a => {
    const statusClass = a.status === 'active' ? 'status-active' : a.status === 'limited' ? 'status-limited' : 'status-off';
    const statusLabel = a.status === 'active' ? 'Online' : a.status === 'limited' ? 'Limited' : 'Offline';
    const model = models.find(m => m.id === a.model);
    return `<div class="agent-card" style="background:rgba(108,99,255,0.05);">
      <div class="icon" style="background:rgba(108,99,255,0.10);">${a.icon}</div>
      <div class="info" style="flex:1;">
        <h4>${a.name} <span class="status-badge ${statusClass}" style="margin-left:8px;font-size:10px;">${statusLabel}</span></h4>
        <p>Provider: ${model ? model.provider : 'N/A'} · Priority ${a.priority}</p>
      </div>
    </div>`;
  }).join('');
}

function renderDashboardStats() {
  document.querySelectorAll('[data-stat]').forEach(el => {
    const key = el.getAttribute('data-stat');
    switch (key) {
      case 'total-users':
        el.textContent = getUsers().length;
        break;
      case 'active-models':
        el.textContent = getModels().filter(m => m.status === 'active').length;
        break;
      case 'active-agents':
        el.textContent = getAgents().filter(a => a.status === 'active').length;
        break;
      case 'total-requests':
        el.textContent = getRequestLog().length || '0';
        break;
    }
  });
}

function renderUsersTable() {
  const tbody = document.getElementById('usersTableBody');
  if (!tbody) return;
  const users = getUsers();
  tbody.innerHTML = users.map(u => {
    const planClass = u.plan === 'pro' ? 'status-active' : u.plan === 'enterprise' ? 'status-limited' : '';
    return `<tr>
      <td style="color:var(--text);font-weight:600;">${u.name}</td>
      <td>${u.email}</td>
      <td><span class="status-badge ${planClass}">${u.plan}</span></td>
      <td><span class="status-badge ${u.role === 'admin' ? 'status-active' : ''}">${u.role}</span></td>
      <td>${u.createdAt ? new Date(u.createdAt).toLocaleDateString() : '—'}</td>
    </tr>`;
  }).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  initModels();
  renderModelTable();
  renderAgentTable();
  renderAgentStatus();
  renderDashboardStats();
  renderUsersTable();
});
