import { Grid, Paper, Typography } from '@mui/material'

const cards = [
  { title: 'Active Clients', value: '—' },
  { title: 'Today Check-ins', value: '—' },
  { title: 'Revenue (30d)', value: '—' }
]

export default function DashboardPage() {
  return (
    <Grid container spacing={3}>
      {cards.map((card) => (
        <Grid item xs={12} sm={4} key={card.title}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle2" color="text.secondary">{card.title}</Typography>
            <Typography variant="h4" sx={{ mt: 1 }}>{card.value}</Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  )
}
