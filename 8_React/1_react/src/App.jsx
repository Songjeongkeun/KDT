import './App.css'
import Avatar from './components/Avatar'
import Profile from './components/Profile'
import InputUser from './components/InputUser'
import UserList from './components/UserList'

function App() {

  return (
    <>
      <Avatar image="https://plus.unsplash.com/premium_photo-1678197937465-bdbc4ed95815?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8JUVDJTgyJUFDJUVCJTlFJThDfGVufDB8fDB8fHww" isNew={true}></Avatar>

      <Avatar image="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" isNew={true}></Avatar>

      <Profile image="https://images.unsplash.com/photo-1499952127939-9bbf5af6c51c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fCVFQyU4MiVBQyVFQiU5RSU4Q3xlbnwwfHwwfHx8MA%3D%3D" name="김사과" title="AI 개발자" isNew={false}/>

      <Profile image="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" name="오렌지" title="백앤드 개발자" isNew={true}/>

      <hr/>
      <InputUser/>

      <hr/>
      <UserList/>
    </>
  )
}

export default App
