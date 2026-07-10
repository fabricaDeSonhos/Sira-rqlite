export const START_HOUR = 8
export const END_HOUR = 22
export const TOTAL_MINUTES = (END_HOUR - START_HOUR) * 60

export function timeToMinutes(time) {
  const [h, m] = time.split(':').map(Number)
  return h * 60 + m
}

export function minutesToTime(minutes) {
  const h = Math.floor(minutes / 60).toString().padStart(2, '0')
  const m = (minutes % 60).toString().padStart(2, '0')
  return `${h}:${m}`
}

export function formatDateBR(dateString) {
  const [y, m, d] = dateString.split('-')
  return `${d}/${m}/${y}`
}

export function addDays(dateString, amount) {
  const date = new Date(`${dateString}T12:00:00`)
  date.setDate(date.getDate() + amount)
  return date.toISOString().slice(0, 10)
}

export function getWeekDates(dateString) {
  const date = new Date(`${dateString}T12:00:00`)
  const day = date.getDay()
  const mondayOffset = day === 0 ? -6 : 1 - day
  const monday = new Date(date)
  monday.setDate(date.getDate() + mondayOffset)
  return Array.from({ length: 7 }, (_, i) => {
    const item = new Date(monday)
    item.setDate(monday.getDate() + i)
    return item.toISOString().slice(0, 10)
  })
}

export function getDayLabel(dateString) {
  const names = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
  const date = new Date(`${dateString}T12:00:00`)
  return names[date.getDay()]
}

export function getOccupationPercent(reservations, artifactId, dateString) {
  const used = reservations
    .filter(r => r.active && r.artifactId === artifactId && r.date === dateString)
    .reduce((acc, r) => acc + (timeToMinutes(r.endTime) - timeToMinutes(r.startTime)), 0)
  return Math.min(100, Math.round((used / TOTAL_MINUTES) * 100))
}
