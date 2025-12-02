import { Box, Toolbar, AppBar, Typography, IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material'
import { Dashboard, People, QrCodeScanner, History, Insights, Settings } from '@mui/icons-material'
import { Route, Routes, Link, useLocation } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import ClientsPage from './pages/ClientsPage'
import VisitsPage from './pages/VisitsPage'
import SubscriptionTypesPage from './pages/SubscriptionTypesPage'

const drawerWidth = 240

const navItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { text: 'Clients', icon: <People />, path: '/clients' },
  { text: 'Visits', icon: <History />, path: '/visits' },
  { text: 'Subscription Types', icon: <QrCodeScanner />, path: '/subscription-types' },
  { text: 'Reports', icon: <Insights />, path: '/reports' },
  { text: 'Settings', icon: <Settings />, path: '/settings' }
]

function Sidebar() {
  const location = useLocation()
  return (
    <Drawer variant="permanent" sx={{ width: drawerWidth, [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' } }}>
      <Toolbar><Typography variant="h6">Gordey GYM</Typography></Toolbar>
      <List>
        {navItems.map((item) => (
          <ListItem button key={item.text} component={Link} to={item.path} selected={location.pathname === item.path}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  )
}

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Gordey GYM Admin
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: `${drawerWidth}px` }}>
        <Toolbar />
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/clients" element={<ClientsPage />} />
          <Route path="/visits" element={<VisitsPage />} />
          <Route path="/subscription-types" element={<SubscriptionTypesPage />} />
        </Routes>
      </Box>
    </Box>
  )
}

export default App
