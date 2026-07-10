import React, { useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import { artifacts, initialReservations } from './data/mockData'
import {
  addDays,
  formatDateBR,
  getDayLabel,
  getOccupationPercent,
  getWeekDates,
  minutesToTime,
  START_HOUR,
  END_HOUR,
  timeToMinutes,
  TOTAL_MINUTES,
} from './utils/dateUtils'

const artifactIcons = {
  'Sala de aula': '▣',
  Laboratório: '♙',
  Auditório: '◉',
  Veículo: '▰',
  'Sala de reunião': '♟',
}

function Header({ currentPage, setCurrentPage, openForm }) {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand-icon">▦</div>
        <strong>Sistema de Reservas</strong>
      </div>

      <nav className="tabs">
        <button className={currentPage === 'daily' ? 'active' : ''} onClick={() => setCurrentPage('daily')}>
          <span>▣</span> Calendário Diário
        </button>
        <button className={currentPage === 'weekly' ? 'active' : ''} onClick={() => setCurrentPage('weekly')}>
          <span>▥</span> Ocupação Semanal
        </button>
        <button className={currentPage === 'table' ? 'active' : ''} onClick={() => setCurrentPage('table')}>
          <span>☷</span> Reservas
        </button>
      </nav>

      <div className="header-actions">
        <button className="primary-button" onClick={() => openForm()}>
          <span>+</span> Nova Reserva
        </button>
        
      </div>
    </header>
  )
}

function ArtifactFilterMenu({ value, onChange, align = 'left' }) {
  const [open, setOpen] = useState(false)
  const selected = value === 'all' ? null : artifacts.find(a => a.id === Number(value))

  function choose(next) {
    onChange(next)
    setOpen(false)
  }

  return (
    <div className={`filter-menu ${align === 'right' ? 'right' : ''}`}>
      <button className={selected ? 'filter-icon active' : 'filter-icon'} onClick={() => setOpen(prev => !prev)} title="Filtrar artefato">
        ⌕
      </button>
      {open && (
        <div className="filter-dropdown">
          <button className={value === 'all' ? 'selected' : ''} onClick={() => choose('all')}>Todos os artefatos</button>
          {artifacts.map(artifact => (
            <button key={artifact.id} className={value === String(artifact.id) ? 'selected' : ''} onClick={() => choose(String(artifact.id))}>
              {artifact.name}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function FilterChip({ artifactFilter, clearFilter }) {
  if (artifactFilter === 'all') return null
  const artifact = artifacts.find(a => a.id === Number(artifactFilter))
  return (
    <div className="active-filter-chip">
      <span>Filtro ativo:</span>
      <strong>{artifact?.name}</strong>
      <button onClick={clearFilter}>× Remover filtro</button>
    </div>
  )
}

function DailyCalendar({ reservations, selectedDate, setSelectedDate, artifactFilter, setArtifactFilter, openForm, openDetails }) {
  const visibleArtifacts = artifactFilter === 'all' ? artifacts : artifacts.filter(a => a.id === Number(artifactFilter))
  const hours = Array.from({ length: END_HOUR - START_HOUR + 1 }, (_, i) => START_HOUR + i)

  function handleEmptyClick(artifactId, event) {
    const rect = event.currentTarget.getBoundingClientRect()
    const x = Math.max(0, Math.min(rect.width, event.clientX - rect.left))
    const minutes = START_HOUR * 60 + Math.floor((x / rect.width) * TOTAL_MINUTES / 30) * 30
    openForm({
      artifactId,
      date: selectedDate,
      startTime: minutesToTime(minutes),
      endTime: minutesToTime(Math.min(minutes + 60, END_HOUR * 60)),
    })
  }

  return (
    <main className="page">
      <section className="top-line">
        <div className="date-nav">
          <button className="nav-square" onClick={() => setSelectedDate(addDays(selectedDate, -1))}>‹</button>
          <div className="date-box"><span>▣</span>{formatDateBR(selectedDate)} ({getDayLabel(selectedDate)})</div>
          <button className="nav-square" onClick={() => setSelectedDate(addDays(selectedDate, 1))}>›</button>
        </div>
        <FilterChip artifactFilter={artifactFilter} clearFilter={() => setArtifactFilter('all')} />
      </section>

      <section className="calendar-card card">
        <div className="timeline-header">
          <div className="artifact-head">
            <span>Artefato</span>
            <ArtifactFilterMenu value={artifactFilter} onChange={setArtifactFilter} />
          </div>
          <div className="hour-heads">
            {hours.map(h => <div key={h}>{String(h).padStart(2, '0')}:00</div>)}
          </div>
        </div>

        {visibleArtifacts.map(artifact => {
          const dayReservations = reservations.filter(r => r.active && r.artifactId === artifact.id && r.date === selectedDate)
          return (
            <div className="timeline-row" key={artifact.id}>
              <div className="artifact-cell">
                
                <div>
                  <strong>{artifact.name}</strong>
                  <span>{artifact.category}</span>
                </div>
              </div>
              <div className="timeline-track" onDoubleClick={(e) => handleEmptyClick(artifact.id, e)}>
                {dayReservations.map(reservation => {
                  const start = timeToMinutes(reservation.startTime) - START_HOUR * 60
                  const duration = timeToMinutes(reservation.endTime) - timeToMinutes(reservation.startTime)
                  return (
                    <button
                      key={reservation.id}
                      className="reservation-block"
                      style={{ left: `${(start / TOTAL_MINUTES) * 100}%`, width: `${(duration / TOTAL_MINUTES) * 100}%` }}
                      onClick={(e) => { e.stopPropagation(); openDetails(reservation) }}
                    >
                      <small>{reservation.startTime} - {reservation.endTime}</small>
                      <strong>{reservation.purpose}</strong>
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </section> 

      <p className="hint"><strong>Como usar</strong><br />Clique duas vezes em um espaço livre para criar uma nova reserva. Clique em uma reserva existente para ver detalhes.</p>
    </main>
  )
}

function WeeklyOccupation({ reservations, selectedDate, setSelectedDate, artifactFilter, setArtifactFilter, goToDailyFiltered }) {
  const weekDates = getWeekDates(selectedDate)
  const visibleArtifacts = artifactFilter === 'all' ? artifacts : artifacts.filter(a => a.id === Number(artifactFilter))

  return (
    <main className="page">
      <section className="top-line week-top">
        <div className="date-nav">
          <button className="nav-square" onClick={() => setSelectedDate(addDays(selectedDate, -7))}>‹</button>
          <div className="week-title">
            <strong>Semana 24</strong>
            <span>{formatDateBR(weekDates[0])} - {formatDateBR(weekDates[6])}</span>
          </div>
          <button className="nav-square" onClick={() => setSelectedDate(addDays(selectedDate, 7))}>›</button>
        </div>
        <ArtifactFilterMenu value={artifactFilter} onChange={setArtifactFilter} align="right" />
      </section>

      <section className="card weekly-card">
        <div className="weekly-grid weekly-head">
          <div>Artefato</div>
          {weekDates.map(date => <div key={date}><strong>{getDayLabel(date)}</strong><span>{formatDateBR(date).slice(0, 5)}</span></div>)}
        </div>

        {visibleArtifacts.map(artifact => (
          <div className="weekly-grid weekly-row" key={artifact.id}>
            <div className="weekly-artifact">
              
              <div><strong>{artifact.name}</strong><span>{artifact.category}</span></div>
            </div>
            {weekDates.map(date => {
              const percent = getOccupationPercent(reservations, artifact.id, date)
              return (
                <button className="occupation-cell" key={date} onClick={() => goToDailyFiltered(date, artifact.id)} title="Abrir calendário diário filtrado">
                  <div className="progress"><span style={{ width: `${percent}%` }} /></div>
                  <strong>{percent}%</strong>
                </button>
              )
            })}
          </div>
        ))}
      </section>

      <p className="hint">Clique sobre a barra de percentual de um dia para visualizar o calendário diário daquele artefato.</p>
    </main>
  )
}

function ReservationsTable({ reservations, artifactFilter, setArtifactFilter, openDetails, openForm, removeReservation }) {
  const [statusFilter, setStatusFilter] = useState('all')
  const filtered = reservations.filter(r =>
    (artifactFilter === 'all' || r.artifactId === Number(artifactFilter)) &&
    (statusFilter === 'all' || String(r.active) === statusFilter)
  )

  return (
    <main className="page">
      <section className="top-line">
        <h2 className="page-title">Reservas cadastradas</h2>
        <div className="table-filters">
          <label>Status<select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}><option value="all">Todos</option><option value="true">Ativas</option><option value="false">Canceladas</option></select></label>
          <ArtifactFilterMenu value={artifactFilter} onChange={setArtifactFilter} align="right" />
        </div>
      </section>

      <section className="card table-card">
        <table>
          <thead><tr><th>Artefato</th><th>Data</th><th>Horário</th><th>Finalidade</th><th>Responsável</th><th>Status</th><th>Ações</th></tr></thead>
          <tbody>
            {filtered.map(r => {
              const a = artifacts.find(x => x.id === r.artifactId)
              return (
                <tr key={r.id}>
                  <td>{a?.name}</td>
                  <td>{formatDateBR(r.date)}</td>
                  <td>{r.startTime} - {r.endTime}</td>
                  <td>{r.purpose}</td>
                  <td>{r.user}</td>
                  <td><span className={r.active ? 'status active' : 'status inactive'}>{r.active ? 'Ativa' : 'Cancelada'}</span></td>
                  <td className="actions"><button onClick={() => openDetails(r)}>Ver</button><button onClick={() => openForm(r)}>Editar</button><button onClick={() => removeReservation(r.id)}>Excluir</button></td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>
    </main>
  )
}

function ReservationModal({ editing, close, save }) {
  const [form, setForm] = useState({
    artifactId: 1,
    user: '',
    date: '2026-06-14',
    startTime: '08:00',
    endTime: '09:00',
    purpose: '',
    category: '',
    active: true,
    obs: '',
    ...editing,
  })

  function update(name, value) {
    setForm(prev => ({ ...prev, [name]: name === 'artifactId' ? Number(value) : value }))
  }

  return (
    <div className="modal-backdrop">
      <form className="modal" onSubmit={e => { e.preventDefault(); save(form) }}>
        <h2>{form.id ? 'Editar reserva' : 'Nova reserva'}</h2>

        <label className="field"><span>Artefato</span><select value={form.artifactId} onChange={e => update('artifactId', e.target.value)}>{artifacts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}</select></label>
        <div className="two">
          <label className="field"><span>Data</span><input type="date" value={form.date} onChange={e => update('date', e.target.value)} /></label>
          <label className="field"><span>Responsável</span><input value={form.user} onChange={e => update('user', e.target.value)} placeholder="Nome do responsável" /></label>
        </div>
        <div className="two">
          <label className="field"><span>Início</span><input type="time" value={form.startTime} onChange={e => update('startTime', e.target.value)} /></label>
          <label className="field"><span>Fim</span><input type="time" value={form.endTime} onChange={e => update('endTime', e.target.value)} /></label>
        </div>
        <label className="field"><span>Finalidade</span><input value={form.purpose} onChange={e => update('purpose', e.target.value)} placeholder="Ex.: Aula de Algoritmos" /></label>
        <label className="field"><span>Categoria</span><input value={form.category} onChange={e => update('category', e.target.value)} placeholder="Ex.: Aula, Reunião, Evento" /></label>
        <label className="field"><span>Observação</span><textarea value={form.obs} onChange={e => update('obs', e.target.value)} /></label>

        <div className="modal-actions">
          <button type="button" onClick={close}>Cancelar</button>
          <button className="primary-button" type="submit">{form.id ? 'Salvar edição' : 'Salvar reserva'}</button>
        </div>
      </form>
    </div>
  )
}

function DetailsModal({ reservation, close, toggleActive, edit }) {
  const artifact = artifacts.find(a => a.id === reservation.artifactId)
  return (
    <div className="modal-backdrop">
      <div className="modal details">
        <h2>{reservation.purpose}</h2>
        <p><strong>Artefato:</strong> {artifact?.name}</p>
        <p><strong>Data:</strong> {formatDateBR(reservation.date)}</p>
        <p><strong>Horário:</strong> {reservation.startTime} - {reservation.endTime}</p>
        <p><strong>Responsável:</strong> {reservation.user}</p>
        <p><strong>Observação:</strong> {reservation.obs || 'Sem observação'}</p>
        <div className="modal-actions">
          <button onClick={close}>Fechar</button>
          <button onClick={() => edit(reservation)}>Editar</button>
          <button className="danger" onClick={() => toggleActive(reservation.id)}>{reservation.active ? 'Cancelar reserva' : 'Reativar reserva'}</button>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [page, setPage] = useState('daily')
  const [selectedDate, setSelectedDate] = useState('2026-06-14')
  const [artifactFilter, setArtifactFilter] = useState('all')
  const [reservations, setReservations] = useState(initialReservations)
  const [editing, setEditing] = useState(null)
  const [details, setDetails] = useState(null)

  function saveReservation(form) {
    if (form.id) setReservations(prev => prev.map(r => r.id === form.id ? form : r))
    else setReservations(prev => [...prev, { ...form, id: Date.now(), active: true }])
    setEditing(null)
  }

  function toggleActive(id) {
    setReservations(prev => prev.map(r => r.id === id ? { ...r, active: !r.active } : r))
    setDetails(null)
  }

  function removeReservation(id) {
    if (confirm('Deseja excluir esta reserva?')) setReservations(prev => prev.filter(r => r.id !== id))
  }

  function goToDailyFiltered(date, artifactId) {
    setSelectedDate(date)
    setArtifactFilter(String(artifactId))
    setPage('daily')
  }

  return (
    <>
      <Header currentPage={page} setCurrentPage={setPage} openForm={(data) => setEditing(data || {})} />
      {page === 'daily' && <DailyCalendar reservations={reservations} selectedDate={selectedDate} setSelectedDate={setSelectedDate} artifactFilter={artifactFilter} setArtifactFilter={setArtifactFilter} openForm={(data) => setEditing(data)} openDetails={setDetails} />}
      {page === 'weekly' && <WeeklyOccupation reservations={reservations} selectedDate={selectedDate} setSelectedDate={setSelectedDate} artifactFilter={artifactFilter} setArtifactFilter={setArtifactFilter} goToDailyFiltered={goToDailyFiltered} />}
      {page === 'table' && <ReservationsTable reservations={reservations} artifactFilter={artifactFilter} setArtifactFilter={setArtifactFilter} openDetails={setDetails} openForm={(data) => setEditing(data || {})} removeReservation={removeReservation} />}
      {editing !== null && <ReservationModal editing={editing} close={() => setEditing(null)} save={saveReservation} />}
      {details && <DetailsModal reservation={details} close={() => setDetails(null)} toggleActive={toggleActive} edit={(r) => { setDetails(null); setEditing(r) }} />}
      <footer>© 2026 Sistema de Reservas - IFC Campus</footer>
    </>
  )
}

createRoot(document.getElementById('root')).render(<App />)
