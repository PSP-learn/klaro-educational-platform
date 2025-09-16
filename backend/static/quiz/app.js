function el(id) { return document.getElementById(id); }
function val(id) { const e = el(id); return e ? e.value : ''; }
function listFromCSV(id) { const v = val(id); return v ? v.split(',').map(s=>s.trim()).filter(Boolean) : []; }
function linesFromTextarea(id) { const e = el(id); if (!e) return []; return e.value.split('\n').map(s=>s.trim()).filter(Boolean); }

function collectSections() {
  const rows = Array.from(document.querySelectorAll('.section-row'));
  return rows.map(r => ({
    name: r.querySelector('.s-name').value || 'Section',
    types: Array.from(r.querySelectorAll('.s-type:checked')).map(x=>x.value),
    count: parseInt(r.querySelector('.s-count').value || '0', 10),
    difficulty: null,
    negative_marking: 0
  }));
}

function buildPayload() {
  const topics = listFromCSV('topics');
  const domain = val('domain') || 'CBSE';
  const grade = val('grade') || null;
  const baseByType = {
    mcq: parseInt(val('bp_mcq') || '0', 10),
    short: parseInt(val('bp_short') || '0', 10),
    long: parseInt(val('bp_long') || '0', 10)
  };
  const cbseByType = {
    single_correct: parseInt(val('bp_single_correct') || '0', 10),
    assertion_reason: parseInt(val('bp_assertion_reason') || '0', 10),
    short2: parseInt(val('bp_short2') || '0', 10),
    long3: parseInt(val('bp_long3') || '0', 10),
    verylong5: parseInt(val('bp_verylong5') || '0', 10),
    case_study: parseInt(val('bp_case_study') || '0', 10)
  };
  const useCbse = domain === 'CBSE' && Object.values(cbseByType).some(v => v > 0);
  const byType = useCbse ? cbseByType : baseByType;
  const marksBase = {
    mcq: parseInt(val('marks_mcq')||'1',10),
    short: parseInt(val('marks_short')||'3',10),
    long: parseInt(val('marks_long')||'5',10)
  };
  const marksCbse = {
    single_correct: parseInt(val('marks_single_correct')||'1',10),
    assertion_reason: parseInt(val('marks_assertion_reason')||'1',10),
    short2: parseInt(val('marks_short2')||'2',10),
    long3: parseInt(val('marks_long3')||'3',10),
    verylong5: parseInt(val('marks_verylong5')||'5',10),
    case_study: parseInt(val('marks_case_study')||'4',10)
  };
  const marks = useCbse ? { ...marksBase, ...marksCbse } : marksBase;
  const payload = {
    domain,
    grade,
    header: val('header') || null,
    instructions: linesFromTextarea('instructions'),
    topics: topics.length ? topics : ['general'],
    subjects: listFromCSV('subjects'),
    cbse_science_streams: listFromCSV('cbse_science_streams'),
    subject: val('subject') || 'Mathematics',
    mode: val('mode') || 'mixed',
    render: val('render') || 'auto',
    scope_filter: val('scope') || null,
    books_dir: val('books_dir') || null,
    // blueprint
    blueprint: {
      total_questions: parseInt(val('bp_total') || '0', 10) || null,
      by_type: byType,
      by_difficulty: {
        easy: parseInt(val('bp_easy') || '0', 10),
        medium: parseInt(val('bp_medium') || '0', 10),
        hard: parseInt(val('bp_hard') || '0', 10)
      },
      duration_minutes: val('bp_duration') ? parseInt(val('bp_duration'), 10) : null
    },
    sections: collectSections(),
    marks,
    include_solutions: (val('include_solutions') === 'Yes'),
    output_engine: val('output_engine') || 'reportlab',
    // UI metadata
    streams: listFromCSV('streams'),
    class_filter: [val('grade')],
    topic_tags: listFromCSV('tags'),
    subtopics: listFromCSV('subtopics'),
    language: val('language') || 'English',
    centers: listFromCSV('centers'),
    // defaults for generator API compatibility
    num_questions: parseInt(val('bp_total') || '10', 10),
    question_types: ['mcq','short','long'],
    difficulty_levels: ['easy','medium','hard']
  };
  return payload;
}

function updateSummary(preview) {
  const totalMarks = preview.totals && typeof preview.totals.total_marks !== 'undefined' ? `<br/>Total Marks: <strong>${preview.totals.total_marks}</strong>` : '';
  el('summary_totals').innerHTML = `Total Questions: <strong>${preview.totals.total_questions}</strong><br/>Duration: <strong>${preview.duration_estimate} minutes</strong>${totalMarks}`;
  const warnEl = el('summary_warnings');
  if (preview.warnings && preview.warnings.length) {
    warnEl.innerHTML = '<ul>' + preview.warnings.map(w => `<li>${w}</li>`).join('') + '</ul>';
  } else { warnEl.textContent = ''; }
}

async function doPreview() {
  const payload = buildPayload();
  const resp = await fetch('/api/quiz/preview', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer demo' }, body: JSON.stringify(payload) });
  if (!resp.ok) throw new Error(await resp.text());
  const data = await resp.json();
  updateSummary(data);
  return data;
}

async function doGenerate() {
  const resEl = el('result');
  resEl.classList.remove('hidden');
  resEl.textContent = 'Generating...';
  try {
    await doPreview();
    const payload = buildPayload();
    const resp = await fetch('/api/quiz/create', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer demo' }, body: JSON.stringify(payload) });
    if (!resp.ok) throw new Error(await resp.text());
    const data = await resp.json();
    let html = '<div><strong>Quiz created.</strong></div>';
    if (data.pdf_questions_file) html += `<div><a class=\"link\" href=\"/api/quiz/${data.quiz_id}/download?file_type=questions\" target=\"_blank\">Download Questions (PDF)</a></div>`;
    if (data.pdf_answers_file) html += `<div><a class=\"link\" href=\"/api/quiz/${data.quiz_id}/download?file_type=answers\" target=\"_blank\">Download Answers (PDF)</a></div>`;
    if (data.pdf_marking_scheme_file) html += `<div><a class=\"link\" href=\"/api/quiz/${data.quiz_id}/download?file_type=marking_scheme\" target=\"_blank\">Download Marking Scheme (PDF)</a></div>`;
    html += `<div>Quiz ID: <code>${data.quiz_id}</code></div>`;
    resEl.innerHTML = html;
  } catch (e) {
    resEl.textContent = 'Failed: ' + (e && e.message ? e.message : e);
  }
}

function addSectionRow(name='Section', types=['mcq'], count=10) {
  const wrap = el('sections');
  const div = document.createElement('div');
  div.className = 'section-row';
  div.innerHTML = `
    <div class="grid">
      <div class="field"><label>Name</label><input class="s-name" type="text" value="${name}" /></div>
      <div class="field"><label>Types</label>
        <label><input class="s-type" type="checkbox" value="mcq" ${types.includes('mcq')?'checked':''}/> MCQ</label>
        <label><input class="s-type" type="checkbox" value="short" ${types.includes('short')?'checked':''}/> Short</label>
        <label><input class="s-type" type="checkbox" value="long" ${types.includes('long')?'checked':''}/> Long</label>
      </div>
      <div class="field"><label>Count</label><input class="s-count" type="number" min="0" value="${count}" /></div>
      <div class="field"><button type="button" class="remove-section">Remove</button></div>
    </div>`;
  div.querySelector('.remove-section').addEventListener('click', () => div.remove());
  wrap.appendChild(div);
}

function setupAccordions() {
  document.querySelectorAll('.acc-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const sel = btn.getAttribute('data-acc');
      const panel = document.querySelector(sel);
      panel.classList.toggle('open');
    });
  });
}

function setupUI() {
  setupAccordions();
  addSectionRow('Section A', ['mcq'], 10);
  addSectionRow('Section B', ['short'], 10);
  addSectionRow('Section C', ['long'], 5);
  el('add_section').addEventListener('click', () => addSectionRow());
  el('btn_preview').addEventListener('click', () => doPreview().catch(err => alert(err.message || err)));
  el('btn_generate').addEventListener('click', () => doGenerate());
}

document.addEventListener('DOMContentLoaded', setupUI);

