# Database Setup Guide

## Complete Database Schema Setup for Student Management System

## Prerequisites
- Supabase account with PostgreSQL database
- Project URL and API keys from Supabase

## Step-by-Step Setup

### Step 1: Access Supabase SQL Editor

1. Login to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Navigate to **SQL Editor** from the left sidebar
4. Click **New Query**

### Step 2: Create Database Tables

Copy the complete SQL schema from `database/schema.sql` and execute it in the Supabase SQL Editor.

#### What This Does:
- Creates 6 main tables (users, students, lecturers, courses, enrollments, attendance)
- Sets up relationships and foreign keys
- Creates necessary indexes for performance
- Enables Row Level Security (RLS)
- Implements RLS policies for data access control
- Creates auto-update triggers for timestamps

### Step 3: Verify Tables Creation

Run this query to verify all tables were created:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Expected tables:
- attendance
- courses
- enrollments
- lecturers
- students
- users

### Step 4: Verify RLS Policies

Run this query to verify RLS policies:

```sql
SELECT schemaname, tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Step 5: Check Indexes

Verify all indexes were created:

```sql
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename;
```

## Database Schema Overview

### Users Table
Stores authenticated user profiles and account information.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user',
    department VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);
```

### Students Table
Stores detailed student information.

```sql
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
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
    status VARCHAR(50) DEFAULT 'active',
    program VARCHAR(255),
    semester INTEGER DEFAULT 1,
    gpa DECIMAL(3, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Lecturers Table
Stores lecturer information.

```sql
CREATE TABLE lecturers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
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
    office_hours TEXT,
    hire_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Courses Table
Stores course information.

```sql
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    description TEXT,
    department VARCHAR(255) NOT NULL,
    semester INTEGER,
    credits INTEGER,
    lecturer_id UUID REFERENCES lecturers(id),
    max_students INTEGER,
    min_students INTEGER,
    status VARCHAR(50) DEFAULT 'active',
    prerequisites TEXT,
    learning_objectives TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Enrollments Table
Tracks student enrollment in courses.

```sql
CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id),
    course_id UUID NOT NULL REFERENCES courses(id),
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'enrolled',
    grade VARCHAR(2),
    final_score DECIMAL(5, 2),
    attendance_percentage DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, course_id)
);
```

### Attendance Table
Tracks attendance records.

```sql
CREATE TABLE attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id),
    course_id UUID NOT NULL REFERENCES courses(id),
    attendance_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'present',
    remarks TEXT,
    marked_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, course_id, attendance_date)
);
```

## Row Level Security (RLS) Policies

All tables have RLS enabled. Policies enforce:

### Users Table
- Users can view their own profile
- Users can update their own profile
- Admins can view all users

### Students Table
- Students can view their own record
- Lecturers and admins can view students
- Admins can manage all students

### Lecturers Table
- Lecturers can view their own profile
- All users can view active lecturers
- Admins can manage lecturers

### Courses Table
- All users can view active courses
- Lecturers can manage their own courses
- Admins can manage all courses

### Enrollments Table
- Students can view their own enrollments
- Lecturers can view enrollments in their courses
- Admins can view all enrollments

### Attendance Table
- Students can view their own attendance
- Lecturers can manage attendance in their courses
- Admins can manage all attendance

## Indexes

The following indexes are created for performance:
- idx_students_user_id
- idx_students_email
- idx_students_student_id
- idx_lecturers_user_id
- idx_lecturers_email
- idx_courses_lecturer_id
- idx_enrollments_student_id
- idx_enrollments_course_id
- idx_attendance_student_id
- idx_attendance_course_id
- idx_attendance_date
- idx_users_email

## Backup and Recovery

### Backup Database
1. Go to Supabase Dashboard → Database → Backups
2. Click "Save a backup now"
3. Name the backup descriptively
4. Click "Create"

### Restore from Backup
1. Go to Backups section
2. Click "Restore" on desired backup
3. Confirm the action
4. Wait for restoration to complete

## Migrations and Updates

### Adding New Fields

```sql
-- Example: Add new column to students table
ALTER TABLE students 
ADD COLUMN middle_name VARCHAR(100);

-- Add with constraint
ALTER TABLE students 
ADD COLUMN document_id VARCHAR(20) UNIQUE NOT NULL DEFAULT 'TEMP';
```

### Modifying Existing Fields

```sql
-- Change column type
ALTER TABLE students 
ALTER COLUMN gpa TYPE DECIMAL(5, 2);

-- Add not null constraint
ALTER TABLE students 
ALTER COLUMN student_id SET NOT NULL;
```

### Creating Triggers

```sql
-- Example: Update modified timestamp
CREATE TRIGGER update_students_updated_at 
BEFORE UPDATE ON students
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();
```

## Testing Database

### Insert Sample Data

```sql
-- Insert test user (you need to create auth user first through Supabase Auth)
INSERT INTO users (id, email, full_name, phone_number, role) 
VALUES (
    'some-uuid-here', 
    'admin@test.com', 
    'Admin User', 
    '+1234567890', 
    'admin'
);

-- Insert test student
INSERT INTO students (
    user_id, 
    student_id, 
    first_name, 
    last_name, 
    email, 
    enrollment_date,
    program,
    semester
) VALUES (
    'some-uuid-here',
    'STU000001',
    'John',
    'Doe',
    'john@test.com',
    CURRENT_DATE,
    'Bachelor of Science in Computer Science',
    1
);
```

### Query Test Data

```sql
-- Get all students
SELECT * FROM students WHERE is_active = TRUE;

-- Get students with attendance
SELECT s.first_name, s.last_name, c.course_name, a.status
FROM students s
JOIN attendance a ON s.id = a.student_id
JOIN courses c ON a.course_id = c.id;

-- Get enrollment statistics
SELECT c.course_name, COUNT(e.id) as enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.course_name;
```

## Performance Optimization

### Query Optimization Tips

1. Always use indexed columns in WHERE clauses
2. Use EXPLAIN to analyze query performance
3. Avoid SELECT * when possible
4. Use pagination for large result sets
5. Create indexes for frequently searched columns

### Monitor Database Performance

1. Go to Supabase Dashboard → Database → Statistics
2. View query performance metrics
3. Check for slow queries
4. Optimize indexes as needed

## Security Configuration

### Enable RLS
✅ Already enabled on all tables in schema.sql

### Manage Policies

View current policies:
```sql
SELECT * FROM pg_policies;
```

Disable policy temporarily (admin only):
```sql
ALTER POLICY "Users can view own profile" ON users DISABLE;
```

Enable policy:
```sql
ALTER POLICY "Users can view own profile" ON users ENABLE;
```

## Troubleshooting

### Issue: RLS Blocking Data Access
**Solution**: Ensure you're authenticated and the user ID matches

### Issue: Unique Constraint Violated
**Solution**: Check that you're not inserting duplicate values

### Issue: Foreign Key Constraint Failed
**Solution**: Ensure referenced records exist before inserting

### Issue: Performance Degradation
**Solution**: Analyze query execution plan with EXPLAIN

## Support Resources

- [Supabase PostgreSQL Guide](https://supabase.com/docs/guides/database)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)

---

**Database schema version 1.0.0**
