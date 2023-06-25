%% jjfunction

function J=jj_func(X)

global a_u b_u a_f b_f m_d_u m_d_f q_u_0 q_f_0 K_u K_f K_u_nor K_f_nor L_h_u L_h_f m_h_u m_h_f g
global L_d_u L_d_f K_t_u K_t_f l_s_u_0 l_s_f_0 d_d a G_h_u G_h_f G_d_u G_d_f

q_u=X(1); q_f=X(2);

j11 = K_t_u + K_f*((L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2)^2 + K_u*((cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2 - (L_h_u*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u))^2 + K_u*(l_s_u_0 - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u))*(L_h_u - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u) + (2*L_h_u*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^3) - g*m_h_u*((2*cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + G_h_u*L_h_u*sin(a + q_u) - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) - g*m_h_f*((2*cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) + K_f*((2*cos(q_f - d_d + q_u)*(L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^3)*(l_s_f_0 - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u));

j12 = K_u*(l_s_u_0 - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u))*(L_h_u - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f)))/sin(q_f - d_d + q_u)^2 + (L_h_u*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^3) - g*m_h_u*((L_d_u*cos(a + q_u)*cos(d_d - q_f) - L_d_f*cos(a + q_u)*cos(q_f) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) - (L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + (cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) - g*m_h_f*((L_d_u*cos(a + q_u)*cos(d_d - q_f) - L_d_f*cos(a + q_u)*cos(q_f) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) - (L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + (cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) + K_f*(l_s_f_0 - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u))*(L_h_f - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u)))/sin(q_f - d_d + q_u)^2 + (L_h_f*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^3) - K_u*((L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2)*((cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2 - (L_h_u*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u)) - K_f*((L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2)*((cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2 - (L_h_f*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u));

j21 = K_u*(l_s_u_0 - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u))*(L_h_u - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f)))/sin(q_f - d_d + q_u)^2 + (L_h_u*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^3) - g*m_h_u*((L_d_u*cos(a + q_u)*cos(d_d - q_f) - L_d_f*cos(a + q_u)*cos(q_f) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) - (L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + (cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) - g*m_h_f*((L_d_u*cos(a + q_u)*cos(d_d - q_f) - L_d_f*cos(a + q_u)*cos(q_f) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) - (L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_d_f*cos(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*cos(a + q_u) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + (cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) + K_f*(l_s_f_0 - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u))*(L_h_f - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u) + (cos(q_f - d_d + q_u)*(L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u)))/sin(q_f - d_d + q_u)^2 + (L_h_f*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^3) - K_u*((L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2)*((cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2 - (L_h_u*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u)) - K_f*((L_h_f*cos(q_f - d_d + q_u) + L_d_u*cos(q_u) - L_d_f*cos(d_d - q_u))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2)*((cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2 - (L_h_f*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u));

j22 = K_t_f + K_u*((L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f))/sin(q_f - d_d + q_u) - (cos(q_f - d_d + q_u)*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^2)^2 + K_f*((cos(q_f - d_d + q_u)*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^2 - (L_h_f*cos(q_f - d_d + q_u))/sin(q_f - d_d + q_u))^2 - g*m_h_f*((2*cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 + G_h_f*L_h_f*sin(a + d_d - q_f) - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) + K_f*(l_s_f_0 - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u))*(L_h_f - (L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u))/sin(q_f - d_d + q_u) + (2*L_h_f*cos(q_f - d_d + q_u)^2)/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_f*sin(q_f - d_d + q_u) + L_d_u*sin(q_u) + L_d_f*sin(d_d - q_u)))/sin(q_f - d_d + q_u)^3) - g*m_h_u*((2*cos(q_f - d_d + q_u)*(L_d_f*sin(a + q_u)*cos(q_f) - L_d_u*sin(a + q_u)*cos(d_d - q_f) + L_d_u*cos(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_d_f*sin(a + q_u)*sin(q_f) + L_d_u*sin(d_d - q_f)*sin(a + q_u) + L_d_u*sin(q_f - d_d + q_u)*sin(a)))/sin(q_f - d_d + q_u)^3) + K_u*((2*cos(q_f - d_d + q_u)*(L_h_u*cos(q_f - d_d + q_u) + L_d_f*cos(q_f) - L_d_u*cos(d_d - q_f)))/sin(q_f - d_d + q_u)^2 - (2*cos(q_f - d_d + q_u)^2*(L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f)))/sin(q_f - d_d + q_u)^3)*(l_s_u_0 - (L_h_u*sin(q_f - d_d + q_u) + L_d_f*sin(q_f) + L_d_u*sin(d_d - q_f))/sin(q_f - d_d + q_u));

J = [j11 j12;
     j21 j22];
end