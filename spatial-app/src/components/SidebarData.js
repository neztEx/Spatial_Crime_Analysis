import { FaHome, FaMapMarkedAlt, FaDatabase } from "react-icons/fa";


export const SidebarData = [
  {
    title: 'Home',
    path: '/welcome',
    icon: <FaHome />,
    cName: 'nav-text'
  },
  {
    title: 'Data Overview',
    path: '/overview',
    icon: <FaDatabase />,
    cName: 'nav-text'
  },
  {
    title: 'Data Visualization',
    path: '/map',
    icon: <FaMapMarkedAlt />,
    cName: 'nav-text'
  }
]
