-- ========================================
-- STUDENT MANAGEMENT SYSTEM DATABASE SCHEMA
-- Supabase PostgreSQL Database
-- ========================================

-- ==================== Users Table ====================
-- Stores authenticated users (created by Supabase Auth)
-- This table extends Supabase Auth with additional profile info
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user', -- 'admin', 'lecturer', 'staff', 'user'
    department VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    last_login TIMESTAMP WITH TIME ZONE
);

-- ==================== Students Table ====================
-- Stores student information
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    blood_group VARCHAR(5),
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'inactive', 'graduated', 'suspended'
    program VARCHAR(255), -- e.g., "Bachelor of Science in Computer Science"
    semester INTEGER DEFAULT 1,
    gpa DECIMAL(3, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW())
);

-- ==================== Lecturers Table ====================
-- Stores lecturer/instructor information
CREATE TABLE IF NOT EXISTS lecturers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    lecturer_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    department VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    qualification VARCHAR(255),
    office_room VARCHAR(50),
    office_phone VARCHAR(20),
    office_hours TEXT, -- e.g., "Mon-Wed 2-4 PM"
    hire_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'inactive', 'on_leave'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW())
);

-- ==================== Courses Table ====================
-- Stores course information
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    description TEXT,
    department VARCHAR(255) NOT NULL,
    semester INTEGER,
    credits INTEGER,
    lecturer_id UUID REFERENCES lecturers(id) ON DELETE SET NULL,
    max_students INTEGER,
    min_students INTEGER,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'inactive', 'archived'
    prerequisites TEXT,
    learning_objectives TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW())
);

-- ==================== Enrollments Table ====================
-- Tracks student enrollment in courses
CREATE TABLE IF NOT EXISTS enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'enrolled', -- 'enrolled', 'completed', 'dropped'
    grade VARCHAR(2),
    final_score DECIMAL(5, 2),
    attendance_percentage DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    UNIQUE(student_id, course_id)
);

-- ==================== Attendance Table ====================
-- Tracks student attendance records
CREATE TABLE IF NOT EXISTS attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'present', -- 'present', 'absent', 'late', 'excused'
    remarks TEXT,
    marked_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC'::TEXT, NOW()),
    UNIQUE(student_id, course_id, attendance_date)
);

-- ==================== Indexes ====================
-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id);
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_student_id ON students(student_id);
CREATE INDEX IF NOT EXISTS idx_lecturers_user_id ON lecturers(user_id);
CREATE INDEX IF NOT EXISTS idx_lecturers_email ON lecturers(email);
CREATE INDEX IF NOT EXISTS idx_courses_lecturer_id ON courses(lecturer_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course_id ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student_id ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_course_id ON attendance(course_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(attendance_date);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ==================== Row Level Security (RLS) ====================
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE lecturers ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;

-- ==================== RLS Policies for Users Table ====================
-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Admins can view all users
CREATE POLICY "Admins can view all users" ON users
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== RLS Policies for Students Table ====================
-- Students can view their own record
CREATE POLICY "Students can view own record" ON students
    FOR SELECT USING (user_id = auth.uid());

-- Lecturers and admins can view students
CREATE POLICY "Lecturers and admins can view students" ON students
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() AND role IN ('admin', 'lecturer')
        )
    );

-- Admins can insert/update/delete students
CREATE POLICY "Admins can manage students" ON students
    FOR ALL USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== RLS Policies for Lecturers Table ====================
-- Lecturers can view their own profile
CREATE POLICY "Lecturers can view own profile" ON lecturers
    FOR SELECT USING (user_id = auth.uid());

-- All authenticated users can view active lecturers
CREATE POLICY "Users can view active lecturers" ON lecturers
    FOR SELECT USING (is_active = TRUE);

-- Admins can manage lecturers
CREATE POLICY "Admins can manage lecturers" ON lecturers
    FOR ALL USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== RLS Policies for Courses Table ====================
-- All authenticated users can view active courses
CREATE POLICY "Users can view active courses" ON courses
    FOR SELECT USING (is_active = TRUE);

-- Lecturers can manage their own courses
CREATE POLICY "Lecturers can manage own courses" ON courses
    FOR ALL USING (
        lecturer_id = (SELECT id FROM lecturers WHERE user_id = auth.uid())
    );

-- Admins can manage all courses
CREATE POLICY "Admins can manage courses" ON courses
    FOR ALL USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== RLS Policies for Enrollments Table ====================
-- Students can view their own enrollments
CREATE POLICY "Students can view own enrollments" ON enrollments
    FOR SELECT USING (
        student_id IN (SELECT id FROM students WHERE user_id = auth.uid())
    );

-- Lecturers can view enrollments in their courses
CREATE POLICY "Lecturers can view course enrollments" ON enrollments
    FOR SELECT USING (
        course_id IN (
            SELECT id FROM courses 
            WHERE lecturer_id = (SELECT id FROM lecturers WHERE user_id = auth.uid())
        )
    );

-- Admins can view all enrollments
CREATE POLICY "Admins can view all enrollments" ON enrollments
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== RLS Policies for Attendance Table ====================
-- Students can view their own attendance
CREATE POLICY "Students can view own attendance" ON attendance
    FOR SELECT USING (
        student_id IN (SELECT id FROM students WHERE user_id = auth.uid())
    );

-- Lecturers can view and manage attendance in their courses
CREATE POLICY "Lecturers can manage course attendance" ON attendance
    FOR ALL USING (
        course_id IN (
            SELECT id FROM courses 
            WHERE lecturer_id = (SELECT id FROM lecturers WHERE user_id = auth.uid())
        )
    );

-- Admins can manage all attendance
CREATE POLICY "Admins can manage all attendance" ON attendance
    FOR ALL USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- ==================== Triggers ====================
-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('UTC'::TEXT, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lecturers_updated_at BEFORE UPDATE ON lecturers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enrollments_updated_at BEFORE UPDATE ON enrollments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_attendance_updated_at BEFORE UPDATE ON attendance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
