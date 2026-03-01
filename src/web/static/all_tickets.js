// ---------------------------
// ALL TICKETS MODALS JS
// ---------------------------

// Confirm (Close) Modal
const confirmModal = document.getElementById('confirmModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const modalForm = document.getElementById('modalForm');
const confirmClose = confirmModal.querySelector('.close');
const cancelBtn = document.getElementById('cancelModal');

// Escalate Modal
const escalateModal = document.getElementById('escalateModal');
const escalateForm = document.getElementById('escalateForm');
const escalateTitle = document.getElementById('escalateTitle');
const closeEscalate = document.getElementById('closeEscalate');
const cancelEscalateBtn = document.getElementById('cancelEscalateBtn');

// ---------------------------
// Helper: Open / Close Modals
// ---------------------------
function openConfirmModal(ticketId) {
    modalTitle.textContent = 'Close Ticket';
    modalMessage.textContent = `Are you sure you want to close ticket #${ticketId}?`;
    modalForm.action = `/close/${ticketId}`;
    confirmModal.style.display = 'flex';
}

function openEscalateModal(ticketId, ticketTitle) {
    escalateTitle.textContent = `Escalate Ticket #${ticketId} - ${ticketTitle}`;
    escalateForm.action = `/escalate/${ticketId}`;
    escalateModal.style.display = 'flex';
}

// Close buttons
confirmClose.onclick = cancelBtn.onclick = () => { confirmModal.style.display = 'none'; };
closeEscalate.onclick = cancelEscalateBtn.onclick = () => { escalateModal.style.display = 'none'; };

// Close modals when clicking outside
window.onclick = (e) => {
    if (e.target === confirmModal) confirmModal.style.display = 'none';
    if (e.target === escalateModal) escalateModal.style.display = 'none';
};

// ---------------------------
// Event Delegation for Buttons
// ---------------------------
document.body.addEventListener('click', (e) => {

    // Close Ticket button
    const closeBtn = e.target.closest('button[data-action="close"]');
    if (closeBtn) {
        const ticketId = closeBtn.dataset.id;
        openConfirmModal(ticketId);
        return;
    }

    // Escalate Ticket button
    const escalateBtn = e.target.closest('button[data-action="escalate"]');
    if (escalateBtn) {
        const ticketId = escalateBtn.dataset.id;
        const ticketTitle = escalateBtn.dataset.title;
        openEscalateModal(ticketId, ticketTitle);
        return;
    }

});