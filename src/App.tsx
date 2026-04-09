import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Overview from './pages/Overview'
import Install from './pages/Install'
import Usage from './pages/Usage'
import Features from './pages/Features'
import Menus from './pages/Menus'
import Skills from './pages/Skills'
import Agents from './pages/Agents'

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/overview" replace />} />
          <Route path="overview" element={<Overview />} />
          <Route path="install" element={<Install />} />
          <Route path="usage" element={<Usage />} />
          <Route path="features" element={<Features />} />
          <Route path="menus" element={<Menus />} />
          <Route path="skills" element={<Skills />} />
          <Route path="agents" element={<Agents />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
