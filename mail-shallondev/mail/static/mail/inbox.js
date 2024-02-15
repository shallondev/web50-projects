// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', function() {
    compose_email('','','');
  });

  // Handle compose form submissions
  document.querySelector('#compose-form').addEventListener('submit', sendEmail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipient, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';

  // Create composition form
  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails for mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // Create div for each email
      email.forEach(singleton => {
        
        // Create a new div
        const emailElement = document.createElement('div');

        // Create a class for CSS styling
        emailElement.classList.add('email-item');

        // Set background color based on read or not
        emailElement.style.backgroundColor = singleton.read ? '#f8f8f8' : 'white';

        // Edit HTML content
        emailElement.innerHTML = `
          <p><strong>${singleton.sender}</strong>   ${singleton.subject}   <span>${singleton.timestamp}</span></p>
        `;
        
        // Stuff when clicked
        emailElement.addEventListener('click', function() {

          // Go to email
          viewEmail(singleton, mailbox);

        });

        // Add emailElement to emails-view
        document.querySelector('#emails-view').append(emailElement);
        });
});
}

function sendEmail(event) {
  // Prevent the default form submission
  event.preventDefault();

  // Store compose form inputs
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send information to the backend
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
}

function viewEmail(clickedEmail, mailbox) {
  console.log("sucessfully loaded email");

  // Show the email contents and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';

  // Load email content from backend
  fetch(`/emails/${clickedEmail.id}`)
  .then(response => response.json())
  .then(email => {
      console.log(email);

      // Show information about email
      document.querySelector('#email-content').innerHTML = `
          <h5>Sent: ${email.sender}</h5>
          <h5>Recipients: ${email.recipients.join(", ")}</h5>
          <h6>${email.timestamp}</h6>
          <p>body: ${email.body}</p>
      `;

      // Reply
      const replyBtn = document.createElement('button');

      // Classes to reply btn
      replyBtn.classList.add('btn', 'btn-sm', 'btn-outline-primary');

      // Add content to button
      replyBtn.innerHTML = 'reply';

      // Add reply to emails-view
      document.querySelector('#email-content').append(replyBtn);

      // replyBtn functionality
      replyBtn.addEventListener('click', function() { 
          compose_email(
            email.sender,
            `Re: ${email.subject}`,
            `On ${email.timestamp} ${email.sender} wrote: ${email.body}`,
          );
      });

      // Archive
      if (mailbox === 'inbox' || mailbox === 'archive'){
        // Create a button
        const archiveBtn = document.createElement('button');
        
        // Set button to display archive or unarchive
        archiveBtn.innerHTML = email.archived ? 'unarchive' : 'archive';

        // Add classes to button
        archiveBtn.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'ml-1');

        // Add archiveBtn to emails-view
        document.querySelector('#email-content').append(archiveBtn);

        archiveBtn.addEventListener('click', function() {
          
          // Archive or unarchive on click
          fetch(`/emails/${clickedEmail.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          })
          
          // Load inbox
          load_mailbox('inbox')
        });
      }
  });

  // Set read to true
  fetch(`/emails/${clickedEmail.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}