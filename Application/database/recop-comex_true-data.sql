-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2019 at 04:26 PM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `recop-comex`
--

--
-- Dumping data for table `user_account`
--

INSERT INTO `user_account` (`id`, `info_id`, `username`, `password`, `email_address`, `type`, `last_active`, `status`) VALUES
(1, 1, 'admin-recop', '$2b$12$aLUMJqDekK/DY8nU5c4y3O2lWmP4.af.YCWeol5Cc.nAgw6Wau7ia', 'recop.baste@gmail.com', 1, '2019-03-08 23:23:11', 'A'),
(2, 2, 'pres.baste', '$2b$12$9kebxlvRAnR/L3Jx9GIcQeDEMuIDrOMlfoIbFNv0lkhpte7RI29WC', 'pres.baste@gmail.com', 5, '2019-03-08 23:23:54', 'A'),
(3, 3, 'fmi.baste', '$2b$12$9DeJoAw7WoF6GMq9d70Tnec2ALPZEuEOa1qSWEL7S.MmJEnrZJrem', 'fmi.baste@gmail.com', 5, '2019-03-08 23:24:45', 'A'),
(4, 4, 'acad.baste', '$2b$12$UtE8pwqmZK3Et9ioHkSoSODiCzNT1cRgsyQcYkhTDxlwBlgOTDs6.', 'acad.baste@gmail.com', 5, '2019-03-07 21:37:01', 'A');

--
-- Dumping data for table `user_information`
--

INSERT INTO `user_information` (`id`, `first_name`, `middle_name`, `last_name`, `company_name`, `bio`, `gender`, `birthday`, `address`, `telephone`, `mobile_number`, `partner_thrust`) VALUES
(1, 'Ana', 'Dula', 'Manzano', 'San Sebastian College Recoletos de Cavite', 'I am the ReCOP Director.', 'F', '1998-01-21', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(2, 'Rafael', 'B.', 'Pecson', 'San Sebastian College Recoletos de Cavite', 'I am the President.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(3, 'James Dexter', 'D.', 'Palagtiosa', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Formation, Mission and Identity.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(4, 'James', 'T.', 'Bumangabang', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Academic Services.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', '', '', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
