package com.example.demo.auth;


import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

//시큐리티 설정에서 loginProcessingUrl("/login");
///login 주소 요청이 오면 자동으로 UserDetailsService 타입으로 IoC되어 있는 loaduserByUsername 함수가 실행
@Service
// @Transactional // 로직을 처리하다가 에러가 발생하면, 변경된 데이터를 로직을 수행하기 이전 상태로 콜백
@RequiredArgsConstructor
public class PrincipalDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    //public User saveUser(User user) {
    //	validateDuplicateUser(user);
    //
    //	return userRepository.save(user);
    //}

    //private void valideateDuplicateUser(User user) {
    //	User findUser = userRepository.findByEmail(user.getEmail());
    //	if(findUser != null) {
    //		throw new IllegalStateException("이미 가입된 회원입니다.");
    //	}
    //}

    // 시큐리티 세션 = Authentication = UserDetails
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException { // input 값에서 name =  "username"을 받아옴
        System.out.println("Username: " + username);
        User userEntity = userRepository.findByUsername(username);
        if(userEntity != null) { // 유저가 있는 경우
            return new PrincipalDetails(userEntity); // Authentication 내부에 들어가게 된다. -> 시큐리티 session에 들어가게 된다.
        }
        return null;
    }

}
