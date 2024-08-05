const getAllUsersBtn = document.querySelector('#get-all-users')

getAllUsersBtn.addEventListener('click', () => {
    fetch('http://127.0.0.1:8000/test/users/?skip=0')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error))
})


// Login
const usernameInput = document.querySelector('#username')
const passwordInput = document.querySelector('#password')
const loginBtn = document.querySelector('#login')
const loginWrp = document.querySelector('#login-wrp')
const userSection = document.querySelector('#user-section')
const invalidSection = document.querySelector('#invalid_username')
const InfoSection = document.querySelector('#info_user_div')
const dataContainer = document.querySelector('#info');
const welcome = document.querySelector('#welcome')
const invalid = document.querySelector('#invalid')
const logoutBtn = document.querySelector('#logout')

const currentUser = () => {
    if (localStorage.getItem('username')) {
        loginWrp.style.display = 'none'
        userSection.style.display = 'block'
        invalidSection.style.display = 'none'
        invalid.innerHTML = ``
        welcome.innerHTML = `Hi, <strong>${localStorage.getItem('username')}</strong>!`
    }
}
const error_notfound = () => {
        invalidSection.style.display = 'block'
        invalid.innerHTML = `Invalid username or password!!`

}

const error_ntlgn = () => {
            localStorage.removeItem('token')
            localStorage.removeItem('username')

            InfoSection.style.display = 'block';
            dataContainer.innerHTML = 'You are not login.Please login'
            loginWrp.style.display = 'block'
            userSection.style.display = 'none'
            welcome.innerHTML = ''
}

currentUser()

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')

    InfoSection.style.display = 'none';
    dataContainer.innerHTML = ''
    loginWrp.style.display = 'block'
    userSection.style.display = 'none'
    welcome.innerHTML = ''
})


loginBtn.addEventListener('click', () => {
    let formData = new FormData()
    InfoSection.style.display = 'none';
    dataContainer.innerHTML = ''
    formData.append('username', usernameInput.value)
    formData.append('password', passwordInput.value)

fetch('http://127.0.0.1:8000/test/token/', {
    method: 'POST',
    body: formData
})
    .then(response => {
        if (!response.ok) {
            if (response.status === 404){
                error_notfound()
                console.log('Invalid username or password')
            }
            if (response.status === 422){
                error_notfound()
                console.log('Invalid username or password')
            }

            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        InfoSection.style.display = 'none';
        dataContainer.innerHTML = ''
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('username', data.username)

        currentUser()
    })
    .catch(error => console.error(error))
})




const Profile_token = document.querySelector('#get-profile-token')


let token = localStorage.getItem('token')
Profile_token.addEventListener('click', () => {
  fetch('http://127.0.0.1:8000/test/profile', {
    headers: {
      Authorization: localStorage.getItem('token')
        ? `Bearer ${localStorage.getItem('token')}`
        : undefined

        },
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401){
                error_ntlgn()
                console.log('You are not login.Please login')
            }


            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
            InfoSection.style.display = 'block';
            dataContainer.innerHTML = ''
            for (const key in data) {
                const paragraph = document.createElement('p');
                paragraph.textContent = `${key}: ${data[key]}`;
                dataContainer.appendChild(paragraph);
            }
            InfoSection.appendChild(dataContainer);
            console.log(data);
        })





        .catch(error => {
            console.error(error)
        })

        })


