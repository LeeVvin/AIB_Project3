package com.example.demo.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnWebApplication;
import org.springframework.boot.autoconfigure.security.ConditionalOnDefaultWebSecurity;
import org.springframework.boot.autoconfigure.security.SecurityProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@SuppressWarnings({ "deprecation", "unused" })
@Configuration // IoC 빈(bean)을 등록
@EnableWebSecurity(debug = true) // 시큐리티 필터 등록
@EnableGlobalMethodSecurity(prePostEnabled = true, securedEnabled = true) // 특정 주소 접근시 권한 및 인증을 위한 어노테이션 활성화
@ConditionalOnDefaultWebSecurity
@ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
public class SecurityConfig{

    // 해당 메서드의 리턴디는 오브젝트를 IoC로 등록해줌
    // BCryptPasswordEncoder는 Spring Security에서 제공하는 비밀번호 암호화 객체
    // 회원 비밀번호 등로 ㄱ시 해당 메서드를 이용하여 암호화 -> 로그인 처리시 동일한 해시로 비교
    @Bean
    public BCryptPasswordEncoder encodePwd() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    @Order(SecurityProperties.BASIC_AUTH_ORDER)
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http.csrf().disable();
        http.authorizeRequests() // 요청 URL에 따라 접근 권한을 설정
                .requestMatchers("/user/**").authenticated()  // 인증만 되면 들어갈 수 있는 주소
                .anyRequest().permitAll() // 나머지 주소는 모든 권한이 허용
                .and()
                .formLogin() // 로그인 폼은
                .loginPage("/loginForm") // 해당 주소로 로그인 페이지를 호출한다.
                //.usernameParameter("\"email\"")
                .loginProcessingUrl("/login") // /login이 호출되면 시큐리티가 낚아채서 대신 로그인을 해줌
                .defaultSuccessUrl("/");

        return http.build();
    }
}