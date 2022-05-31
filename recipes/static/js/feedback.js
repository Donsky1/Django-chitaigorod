var formElement = document.querySelector('#form')

function feedbackHandler()
{
    alert('Сообщение успешно отправлено!')
}

formElement.addEventListener('submit', feedbackHandler)