
How it Works      Simple Policy
Your code found these existing notes.

You can edit, erase, and save your changes.


import { useState } from "react";

function StudentForm(){
      const [formData,setFormData] = useState({
    name:"",
    age:"",
    email:"",
    course:""
  });
  const [errors,setErrors] = useState([]);
  const handleChange = (e)=>{
      const name = e.target.name;
      const value = e.target.value;
      setFormData({
            ...formData,
            [name]:value
      });
  };
  const handleSubmit = ()=>{
      const newErrors = {};
      if(formData.name.trim()===""){
            newErrors.name="Name is Required";
      }
      if(formData.age===""){
            newErrors.age="Age is Required";
      }
      if(formData.course.trim()===""){
            newErrors.course="Course is Required";
      }
      if(formData.email.trim()===""){
            newErrors.email="Email is Required";
      }
      setErrors(newErrors);
      console.log(formData);
      setFormData({
            name:"",
            age:"",
            email:"",
            course:""
      });
  }
  return(
    <div>
      <h2>Student Registration Form</h2>


      <label>Name</label>
      <input type="text"
       placeholder="Enter Your Name"
       name="name"
       value={formData.name}
       onChange={handleChange}
       />
       <p>{errors.name}</p>
       <br/>


       <label>Age</label>
      <input type="number"
       placeholder="Enter Your Age"
       name="age"
       value={formData.age}
       onChange={handleChange}    
       />
       <p>{errors.age}</p>
       <br/>


       <label>Course</label>
      <input type="text"
       placeholder="Enter Your Course"
       name="course"
       value={formData.course}
       onChange={handleChange}    
       />
       <p>{errors.course}</p>
       <br/>


       <label>Email</label>
      <input type="email"
       placeholder="Enter Your email"
       name="email"
       value={formData.email}
       onChange={handleChange}    
       />
       <p>{errors.email}</p>
       <br/>
      <button onClick={handleSubmit}>Register</button>
    </div>
  );
}
export default StudentForm;
Lock This Pad
You can lock this Coded Pad™ by encrypting the already-encrypted notes with a second code.

Go to the settings tab to lock this pad or see other options.

Government-Proof
Only you know the code (AKA the encryption key) to decrypt the data we store.

Even if the government tortured us, we can't decrypt anything.
Char count
2,063 / 500000
[ Ctrl+Alt+S ]	[ Ctrl+S ]	[ Alt+F5 ]	[ Esc ]
 
 
Discover more
Secure note taking
Language Resources
Fast note saving


fx
ON

No Accounts
Start a pad with one code, start another with another. 
Only You Can Read
Notes are encrypted with your code, not ours. So only you can decrypt your notes.

The Technology

The first time you enter your code, the code creates a secret location in our  database.

Before saving your notes, your code translates your notes into an encrypted version.

✔ Only the encrypted version is saved.
✘ The original notes and ✘ your code is never saved.

This means that only you hold the missing piece (your code) to find the secret location and translate the encrypted version back to its original version.

Sharing & Copyright
Sharing a Coded Pad™ means sharing a code. If you find it, you can delete it yourself. 
It's Everywhere
Just enter one code and start taking notes now! Use the same code to return to it later.
Discover more
Printing & Publishing
Unique code system
Digital notepad service
Our Simple Policy
Free to use, always.
We do not store your codes and we do not want to.
In the event our entire server is compromised, your pads are unreadable because only you hold the codes to find and decrypt your pads (as long as you used unique and un-guessable pads).
In the event the  government wants to read our database, your pads are unreadable because only you hold the codes to find and decrypt them.
We don't care what you store in your pads because we don't know and we can't check. Only you hold the code.
If you find a pad that contains your intellectual property, just delete it yourself. If you can find it, you can edit it.
We are not responsible for the following:
If you use a pad that has a simple and common code like '0000' and someone else accesses it.
If someone by chance uses your same un-guessable code and finds your pad.
Even though all data is backed up and replicated to multiple locations, if an act of God or some hardware failure causes all our servers and backups to be destroyed.
Discover more
Computer Security
Visual Art & Design
Encryption software
^ Back To Top ^

© 2014 - 2026 Coded Pad™. All Rights Reserved.
Questions or Feedback? Email Us

❤️ Support us


Encrypted note service