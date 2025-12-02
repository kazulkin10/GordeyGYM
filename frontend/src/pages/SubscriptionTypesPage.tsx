import { useEffect, useState } from 'react'
import api from '../api'
import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, Paper, TextField, Typography } from '@mui/material'

interface SubscriptionType {
  id: number
  name: string
  price: number
  duration_days?: number
  visit_count?: number
}

export default function SubscriptionTypesPage() {
  const [types, setTypes] = useState<SubscriptionType[]>([])
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ name: '', price: 0, duration_days: 30, visit_count: undefined as number | undefined })

  const load = async () => {
    const res = await api.get('/api/subscriptions/types')
    setTypes(res.data)
  }

  useEffect(() => { load() }, [])

  const submit = async () => {
    await api.post('/api/subscriptions/types', form)
    setOpen(false)
    load()
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Subscription Types</Typography>
        <Button variant="contained" onClick={() => setOpen(true)}>New Type</Button>
      </Box>
      <Grid container spacing={2}>
        {types.map((type) => (
          <Grid item xs={12} md={6} key={type.id}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">{type.name}</Typography>
              <Typography color="text.secondary">Price: {type.price}</Typography>
              <Typography color="text.secondary">Duration: {type.duration_days || '—'} days</Typography>
              <Typography color="text.secondary">Visits: {type.visit_count ?? 'Unlimited'}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>New Subscription Type</DialogTitle>
        <DialogContent>
          <TextField margin="dense" label="Name" fullWidth value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <TextField margin="dense" label="Price" type="number" fullWidth value={form.price} onChange={(e) => setForm({ ...form, price: Number(e.target.value) })} />
          <TextField margin="dense" label="Duration days" type="number" fullWidth value={form.duration_days} onChange={(e) => setForm({ ...form, duration_days: Number(e.target.value) })} />
          <TextField margin="dense" label="Visit count" type="number" fullWidth value={form.visit_count ?? ''} onChange={(e) => setForm({ ...form, visit_count: e.target.value === '' ? undefined : Number(e.target.value) })} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={submit}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
