import { useEffect, useState } from 'react'
import api from '../api'
import { Box, Button, Paper, Stack, TextField, Typography } from '@mui/material'

interface Visit {
  id: number
  client_id: number
  direction: string
  timestamp: string
}

export default function VisitsPage() {
  const [visits, setVisits] = useState<Visit[]>([])
  const [barcode, setBarcode] = useState('')
  const [status, setStatus] = useState('')

  const load = async () => {
    const res = await api.get('/api/visits')
    setVisits(res.data)
  }

  useEffect(() => { load() }, [])

  const handleScan = async () => {
    try {
      await api.post(`/api/visits/scan/${barcode}`)
      setStatus('Scan successful')
      setBarcode('')
      load()
    } catch (err: any) {
      setStatus(err.response?.data?.detail || 'Scan failed')
    }
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>Check-in / Check-out</Typography>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} sx={{ mb: 2 }}>
        <TextField label="Barcode" value={barcode} onChange={(e) => setBarcode(e.target.value)} fullWidth />
        <Button variant="contained" onClick={handleScan}>Scan</Button>
      </Stack>
      {status && <Typography color="text.secondary" sx={{ mb: 2 }}>{status}</Typography>}
      <Stack spacing={1}>
        {visits.map((visit) => (
          <Paper key={visit.id} sx={{ p: 2 }}>
            <Typography>Client #{visit.client_id} — {visit.direction.toUpperCase()}</Typography>
            <Typography color="text.secondary">{new Date(visit.timestamp).toLocaleString()}</Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  )
}
