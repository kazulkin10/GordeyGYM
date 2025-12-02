import { useEffect, useState } from 'react'
import api from '../api'
import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, Paper, TextField, Typography } from '@mui/material'

interface Client {
  id: number
  full_name: string
  phone?: string
  barcode?: string
  balance?: number
  vip?: boolean
}

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ full_name: '', phone: '', barcode: '' })

  const load = async () => {
    try {
      const res = await api.get('/api/clients')
      setClients(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async () => {
    await api.post('/api/clients', form)
    setOpen(false)
    setForm({ full_name: '', phone: '', barcode: '' })
    load()
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Clients</Typography>
        <Button variant="contained" onClick={() => setOpen(true)}>New Client</Button>
      </Box>
      <Grid container spacing={2}>
        {clients.map((client) => (
          <Grid item xs={12} md={6} key={client.id}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">{client.full_name}</Typography>
              <Typography variant="body2" color="text.secondary">Phone: {client.phone || '—'}</Typography>
              <Typography variant="body2" color="text.secondary">Barcode: {client.barcode || '—'}</Typography>
              <Typography variant="body2" color="text.secondary">Balance: {client.balance ?? 0}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>New Client</DialogTitle>
        <DialogContent>
          <TextField margin="dense" label="Full name" fullWidth value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <TextField margin="dense" label="Phone" fullWidth value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <TextField margin="dense" label="Barcode" fullWidth value={form.barcode} onChange={(e) => setForm({ ...form, barcode: e.target.value })} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleSubmit}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
