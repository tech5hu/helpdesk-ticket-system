// ===== Generic Confirm Modal =====
const confirmModal = document.getElementById('confirmModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const modalForm = document.getElementById('modalForm');
const confirmClose = confirmModal.querySelector('.close');
const cancelBtn = document.getElementById('cancelModal');

function openConfirmModal(title, message, formAction) {
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modalForm.action = formAction;
    confirmModal.style.display = 'flex';
}

confirmClose.onclick = () => confirmModal.style.display = 'none';
cancelBtn.onclick = () => confirmModal.style.display = 'none';

// ===== Full-screen Escalate Modal =====
const escalateModal = document.getElementById('escalateModal');
const escalateForm = document.getElementById('escalateForm');
const closeEscalate = document.getElementById('closeEscalate');
const cancelEscalateBtn = document.getElementById('cancelEscalateBtn');
const escalateTitle = document.getElementById('escalateTitle');

function openEscalateModal(ticketId, ticketTitle) {
    escalateTitle.textContent = `Escalate Ticket #${ticketId} - ${ticketTitle}`;
    escalateForm.action = `/escalate/${ticketId}`; // replace with Flask url_for if needed
    escalateModal.style.display = 'flex';
}

closeEscalate.onclick = () => escalateModal.style.display = 'none';
cancelEscalateBtn.onclick = () => escalateModal.style.display = 'none';

// ===== Close modals when clicking outside =====
window.onclick = (event) => {
    if(event.target == confirmModal) confirmModal.style.display = 'none';
    if(event.target == escalateModal) escalateModal.style.display = 'none';
};