// update modal
const updateModal = document.getElementById('updateModal');
const updateBtn = document.getElementById('updateBtn');
const closeUpdate = document.getElementById('closeUpdate');
const updateForm = updateModal.querySelector('form');

// create confirmation modal for updates
const updateConfirmModal = document.createElement('div');
updateConfirmModal.classList.add('modal');
updateConfirmModal.style.display = 'none';
updateConfirmModal.innerHTML = `
    <div class="modal-content">
        <h3>Confirm Update</h3>
        <p>Are you sure you want to update this ticket?</p>
        <div class="modal-buttons" style="text-align:center; margin-top:12px;">
            <button id="confirmYes" class="btn">Yes</button>
            <button id="confirmNo" class="btn">No</button>
        </div>
    </div>
`;
document.body.appendChild(updateConfirmModal);

const confirmYes = updateConfirmModal.querySelector('#confirmYes');
const confirmNo = updateConfirmModal.querySelector('#confirmNo');

updateBtn.onclick = () => updateModal.style.display = 'flex';
closeUpdate.onclick = () => updateModal.style.display = 'none';

// update form confirmation
updateForm.addEventListener('submit', e => {
    e.preventDefault();
    updateModal.style.display = 'none';
    updateConfirmModal.style.display = 'flex';
});

confirmYes.onclick = () => { updateConfirmModal.style.display = 'none'; updateForm.submit(); };
confirmNo.onclick = () => { updateConfirmModal.style.display = 'none'; updateModal.style.display = 'flex'; };

// delete modal
const deleteModal = document.getElementById("deleteModal");
const deleteForm = document.getElementById("deleteForm");
const closeDelete = document.getElementById("closeDeleteModal");
const cancelDelete = document.getElementById("cancelDeleteBtn");

function openDeleteModal(ticketId) {
    deleteForm.action = `/delete_ticket/${ticketId}`; // Flask route
    deleteModal.style.display = "flex";
}

closeDelete.onclick = () => deleteModal.style.display = "none";
cancelDelete.onclick = () => deleteModal.style.display = "none";

// confirm modal
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

// esclate modal
const escalateModal = document.getElementById('escalateModal');
const escalateBtn = document.getElementById('escalateBtn');
const escalateClose = document.getElementById('closeEscalate');
const cancelEscalateBtn = document.getElementById('cancelEscalateBtn');

if (escalateBtn) escalateBtn.onclick = () => escalateModal.style.display = 'flex';
if (escalateClose) escalateClose.onclick = () => escalateModal.style.display = 'none';
if (cancelEscalateBtn) cancelEscalateBtn.onclick = () => escalateModal.style.display = 'none';

// Success modal
const successModal = document.getElementById('successModal');
const successClose = successModal.querySelector('.close');
const successCloseBtn = document.getElementById('successCloseBtn');
const successMessage = document.getElementById('successMessage');

function showSuccess(message) {
    successMessage.textContent = message;
    successModal.style.display = 'flex';
}

successClose.onclick = () => successModal.style.display = 'none';
successCloseBtn.onclick = () => successModal.style.display = 'none';

// Click outside to close
window.onclick = (event) => { 
    if(event.target === updateModal) updateModal.style.display = 'none';
    if(event.target === updateConfirmModal) updateConfirmModal.style.display = 'none';
    if(event.target === deleteModal) deleteModal.style.display = 'none';
    if(event.target === confirmModal) confirmModal.style.display = 'none';
    if(event.target === escalateModal) escalateModal.style.display = 'none';
    if(event.target === successModal) successModal.style.display = 'none';
};