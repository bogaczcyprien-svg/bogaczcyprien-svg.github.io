// nav.js – inject shared nav + protect projet pages
(function(){
  const currentPage = location.pathname.split('/').pop() || 'index.html';

  // Pages that require login
  const PROTECTED = ['projets-patrimoine.html','projets-incidents.html','projets-presence.html',
    'projets-mode-projet.html','projets-service.html','projets-dev-pro.html'];

  // Redirect to login if not authenticated
  if(PROTECTED.includes(currentPage) && sessionStorage.getItem('portfolio_access')!=='1'){
    location.href = 'login.html?next=' + currentPage;
  }

  function navLink(page, label, icon=''){
    const isProtected = PROTECTED.includes(page);
    const href = isProtected ? `login.html?next=${page}` : page;
    const cls = currentPage===page ? ' class="active"' : '';
    return `<li><a href="${href}"${cls}>${icon}${label}</a></li>`;
  }

  const nav = `
  <nav>
    <div class="nav-inner">
      <a class="nav-logo" href="index.html"><span>~/</span>theo.durand</a>
      <ul class="nav-links">
        <li><a href="presentation.html" ${currentPage==='presentation.html'?'class="active"':''}>Présentation</a></li>
        <li><a href="bts-sio-sisr.html" ${currentPage==='bts-sio-sisr.html'?'class="active"':''}>BTS SIO SISR</a></li>
        <li><a href="veille.html" ${currentPage==='veille.html'?'class="active"':''}>Veille technologique</a></li>
        <li class="nav-dropdown">
          <span>Mes projets ▾</span>
          <div class="dropdown-menu">
            <a href="login.html?next=projets-patrimoine.html"><span class="dm-title">🖥️ Gérer le patrimoine informatique</span><span class="dm-sub">Inventaire, maintenance, gestion du parc</span></a>
            <a href="login.html?next=projets-incidents.html"><span class="dm-title">🔧 Répondre aux incidents et aux demandes</span><span class="dm-sub">Assistance, support, évolutions</span></a>
            <a href="login.html?next=projets-presence.html"><span class="dm-title">🌐 Développer la présence en ligne</span><span class="dm-sub">Web, services en ligne, communication</span></a>
            <a href="login.html?next=projets-mode-projet.html"><span class="dm-title">📋 Travailler en mode projet</span><span class="dm-sub">Gestion de projet, planification</span></a>
            <a href="login.html?next=projets-service.html"><span class="dm-title">⚙️ Mettre à disposition un service</span><span class="dm-sub">Déploiement, infrastructure, services</span></a>
            <a href="login.html?next=projets-dev-pro.html"><span class="dm-title">📈 Organiser son développement professionnel</span><span class="dm-sub">Formation, veille, certifications</span></a>
          </div>
        </li>
        <li><a href="e6.html" ${currentPage==='e6.html'?'class="active"':''}>Épreuve E6</a></li>
      </ul>
    </div>
  </nav>`;
  document.body.insertAdjacentHTML('afterbegin', nav);
})();
