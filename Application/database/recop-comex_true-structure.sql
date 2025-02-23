-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2019 at 04:27 PM
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

-- --------------------------------------------------------

--
-- Table structure for table `audit_trail`
--

CREATE TABLE `audit_trail` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `affected_id` int(11) NOT NULL,
  `target` varchar(20) NOT NULL,
  `date_created` datetime NOT NULL,
  `type` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `community`
--

CREATE TABLE `community` (
  `id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  `occupation` varchar(30) DEFAULT NULL,
  `income` decimal(10,2) NOT NULL,
  `religion` varchar(20) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `donation`
--

CREATE TABLE `donation` (
  `id` int(11) NOT NULL,
  `sponsee_id` int(11) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `sponsor_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `date_given` datetime NOT NULL,
  `transaction_slip` varchar(200) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_attachment`
--

CREATE TABLE `event_attachment` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `path` varchar(200) NOT NULL,
  `type` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_information`
--

CREATE TABLE `event_information` (
  `id` int(11) NOT NULL,
  `organizer_id` int(11) DEFAULT NULL,
  `name` varchar(30) NOT NULL,
  `description` varchar(140) NOT NULL,
  `objective` varchar(140) NOT NULL,
  `budget` decimal(10,2) NOT NULL,
  `location` varchar(50) NOT NULL,
  `event_date` datetime NOT NULL,
  `participant_no` int(11) NOT NULL,
  `min_age` int(11) NOT NULL,
  `max_age` int(11) NOT NULL,
  `thrust` int(11) NOT NULL,
  `type` int(1) NOT NULL,
  `event_status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_participation`
--

CREATE TABLE `event_participation` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `participant_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `comment` varchar(140) DEFAULT NULL,
  `is_target` char(1) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_photo`
--

CREATE TABLE `event_photo` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `photo` varchar(200) NOT NULL,
  `description` varchar(140) DEFAULT NULL,
  `is_used` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `email_address` varchar(60) NOT NULL,
  `contact_no` varchar(15) DEFAULT NULL,
  `query` varchar(140) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `donation_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `in_stock` int(11) NOT NULL,
  `given` int(11) NOT NULL,
  `expired` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_type`
--

CREATE TABLE `inventory_type` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `body` varchar(140) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `proposal_tracker`
--

CREATE TABLE `proposal_tracker` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `proposed_on` datetime NOT NULL,
  `recop_accepted` datetime DEFAULT NULL,
  `acad_signed` datetime DEFAULT NULL,
  `fmi_signed` datetime DEFAULT NULL,
  `approved_on` datetime DEFAULT NULL,
  `comment` varchar(20) DEFAULT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `referral`
--

CREATE TABLE `referral` (
  `id` int(11) NOT NULL,
  `referrer_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  `type` int(1) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_account`
--

CREATE TABLE `user_account` (
  `id` int(11) NOT NULL,
  `info_id` int(11) DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  `type` int(1) NOT NULL,
  `last_active` datetime NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_information`
--

CREATE TABLE `user_information` (
  `id` int(11) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `bio` varchar(160) DEFAULT NULL,
  `gender` char(1) NOT NULL,
  `birthday` date NOT NULL,
  `address` varchar(100) NOT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `partner_thrust` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_photo`
--

CREATE TABLE `user_photo` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `path` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_trail`
--
ALTER TABLE `audit_trail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `community`
--
ALTER TABLE `community`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `donation`
--
ALTER TABLE `donation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_attachment`
--
ALTER TABLE `event_attachment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_information`
--
ALTER TABLE `event_information`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_participation`
--
ALTER TABLE `event_participation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_photo`
--
ALTER TABLE `event_photo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory_type`
--
ALTER TABLE `inventory_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `proposal_tracker`
--
ALTER TABLE `proposal_tracker`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `referral`
--
ALTER TABLE `referral`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_information`
--
ALTER TABLE `user_information`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_photo`
--
ALTER TABLE `user_photo`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_trail`
--
ALTER TABLE `audit_trail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `community`
--
ALTER TABLE `community`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `donation`
--
ALTER TABLE `donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_attachment`
--
ALTER TABLE `event_attachment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_information`
--
ALTER TABLE `event_information`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_participation`
--
ALTER TABLE `event_participation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_photo`
--
ALTER TABLE `event_photo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_type`
--
ALTER TABLE `inventory_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `proposal_tracker`
--
ALTER TABLE `proposal_tracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `referral`
--
ALTER TABLE `referral`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_account`
--
ALTER TABLE `user_account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_information`
--
ALTER TABLE `user_information`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_photo`
--
ALTER TABLE `user_photo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
